"""SAXO API wrapper for SAXO Bank OpenAPI."""

import json
import logging
import time
from collections.abc import Iterator
from threading import Lock
from typing import Any

import requests  # type: ignore

from .exceptions import OpenAPIError

ITER_LINES_CHUNKSIZE = 60

TRADING_ENVIRONMENTS = {
    "simulation": {
        "stream": "https://streaming.saxobank.com",
        "api": "https://gateway.saxobank.com",
        "prefix": "sim",
    },
    "live": {
        "stream": "https://streaming.saxobank.com",
        "api": "https://gateway.saxobank.com",
    },
}

DEFAULT_HEADERS = {"Accept-Encoding": "gzip, deflate"}

logger = logging.getLogger(__name__)


def mk_endpoint(endpoint: Any, env: str, ep_type: str) -> str:
    base = TRADING_ENVIRONMENTS[env][ep_type]
    # endpointがインスタンスなら.urlまたは.URL属性を使う。なければstr(endpoint)でパス扱い
    if hasattr(endpoint, "url"):
        path = endpoint.url
    elif hasattr(endpoint, "URL"):
        path = endpoint.URL
    else:
        path = str(endpoint)
    if env == "simulation":
        return f"{base}/sim/{path.lstrip('/')}"
    else:
        return f"{base}/{path.lstrip('/')}"


class RateLimiter:
    def __init__(self) -> None:
        # Track all rate limit dimensions
        self.limits = {
            "AppDay": {"remaining": 10000000, "reset": 0},  # 1日1000万リクエスト
            "Session": {"remaining": 120, "reset": 0},  # 1分120リクエスト
            "SessionOrders": {"remaining": 1, "reset": 0},  # 注文系1秒1リクエスト
        }
        self.lock = Lock()
        self.LOW_REQUESTS_THRESHOLD = 10  # Threshold for adding extra delay

    def update_limits(self, headers: dict[str, str]) -> None:
        """Update rate limits based on response headers for all dimensions"""
        with self.lock:
            # Update all supported dimensions
            for dimension in self.limits.keys():
                remaining_header = f"X-RateLimit-{dimension}-Remaining"
                reset_header = f"X-RateLimit-{dimension}-Reset"

                if remaining_header in headers:
                    self.limits[dimension]["remaining"] = int(headers[remaining_header])

                if reset_header in headers:
                    self.limits[dimension]["reset"] = int(headers[reset_header])

    def wait_if_needed(self) -> None:
        """Wait if we're close to hitting rate limits for any dimension"""
        with self.lock:
            # Check all dimensions and find the most restrictive one
            most_restrictive = None
            min_remaining_ratio = float("inf")

            # Define threshold ratios for each dimension
            thresholds = {
                "AppDay": 1000,  # Wait if less than 1000 requests remaining for the day
                "Session": 1,  # Wait if less than 1 request remaining for the minute
                "SessionOrders": 1,  # Wait if less than 1 order remaining for the second
            }

            for dimension, limit_info in self.limits.items():
                remaining = limit_info["remaining"]
                threshold = thresholds.get(dimension, 1)

                if remaining <= threshold:
                    # This dimension is at or below threshold
                    reset_time = limit_info["reset"]
                    if reset_time > 0:
                        logger.info(f"Rate limit threshold reached for {dimension}. Remaining: {remaining}, Reset in: {reset_time} seconds")
                        time.sleep(reset_time)
                        return
                elif remaining <= self.LOW_REQUESTS_THRESHOLD and dimension == "Session":
                    # Special handling for Session dimension - add small delay when getting low
                    logger.info(f"Session rate limit getting low ({remaining} remaining). Adding 1 second delay")
                    time.sleep(1)
                    return


class API:
    r"""API - class to handle APIRequests objects to access API endpoints."""

    def __init__(
        self,
        access_token: str | None,
        environment: str = "simulation",
        headers: dict[str, str] | None = None,
        request_params: dict[str, Any] | None = None,
    ) -> None:
        """Instantiate an API-client instance of saxo_openapi API wrapper.

        Parameters
        ----------
        access_token : string
            Provide a valid access token.

        environment : dict
            Provide the environment for saxo_openapi REST api. Valid values:
            {'api': 'https://gateway.saxobank.com'}

        headers : dict (optional)
            Provide request headers to be set for a request.


        .. note::

            There is no need to set the 'Content-Type: application/json'
            for the endpoints that require this header. The API-request
            classes covering those endpoints will take care of the header.

        request_params : (optional)
            parameters to be passed to the request. This can be used to apply
            for instance a timeout value:

               request_params={"timeout": 0.1}

            See specs of the requests module for full details of possible
            parameters.

        .. warning::
            parameters belonging to a request need to be set on the
            requestinstance and are NOT passed via the client.

        """
        logger.info("setting up API-client for environment %s", environment)
        try:
            TRADING_ENVIRONMENTS[environment]
        except KeyError as e:  # noqa F841
            logger.error("unkown environment %s", environment)
            raise KeyError(f"Unknown environment: {environment}")
        else:
            self.environment = environment

        self.access_token = access_token
        self.environment = environment
        self.client = requests.Session()
        self.client.stream = False
        self._request_params = request_params if request_params else {}
        self.rate_limiter = RateLimiter()

        # personal token authentication
        if self.access_token:
            self.client.headers["Authorization"] = "Bearer " + self.access_token

        self.client.headers.update(DEFAULT_HEADERS)
        if headers:
            self.client.headers.update(headers)
            logger.info("applying headers %s", ",".join(headers.keys()))

    @property
    def request_params(self) -> dict[str, Any]:
        """request_params property."""
        return self._request_params

    def _detect_limiting_dimension(self, headers: dict[str, str], url: str) -> str:
        """Detect which rate limit dimension actually caused the 429 error.

        Args:
            headers: Response headers containing rate limit information
            url: The URL that was rate limited

        Returns:
            str: The dimension that likely caused the rate limit ('AppDay', 'Session', 'SessionOrders')
        """
        # Dynamically discover all rate limit dimensions from headers
        remaining_counts = {}
        for header_name, header_value in headers.items():
            if header_name.startswith("X-RateLimit-") and header_name.endswith("-Remaining"):
                # Extract dimension name: X-RateLimit-{dimension}-Remaining
                dimension = header_name[12:-10]  # Remove 'X-RateLimit-' and '-Remaining'
                remaining_counts[dimension] = int(header_value)

        # Identify which dimension(s) are at 0 or very low
        exhausted_dimensions = []
        for dimension, remaining in remaining_counts.items():
            if remaining == 0:
                exhausted_dimensions.append(dimension)

        # If exactly one dimension is exhausted, that's our answer
        if len(exhausted_dimensions) == 1:
            return exhausted_dimensions[0]

        # If multiple dimensions are exhausted, use endpoint-based heuristics
        if len(exhausted_dimensions) > 1:
            # For order/trade endpoints, prioritize trade/order related dimensions
            if "/orders" in url or "/trade/" in url:
                # Look for dimensions with trade/order keywords
                for dim in exhausted_dimensions:
                    if any(keyword in dim.lower() for keyword in ["trade", "order", "post"]):
                        return dim

                # Fallback to Session-like dimensions
                for dim in exhausted_dimensions:
                    if "session" in dim.lower():
                        return dim

            # For other endpoints, prefer Session-like dimensions
            else:
                for dim in exhausted_dimensions:
                    if "session" in dim.lower():
                        return dim

            # Return the first non-AppDay dimension if possible
            for dim in exhausted_dimensions:
                if dim != "AppDay":
                    return dim

            # Fall back to the first exhausted dimension
            return exhausted_dimensions[0]

        # If no dimensions show as exhausted, use endpoint-based prediction
        # This can happen if the headers aren't perfectly synchronized with the limit
        # or if Remaining headers are missing entirely

        # Dynamically discover all available dimensions from reset headers
        available_dimensions = []
        for header_name in headers:
            if header_name.startswith("X-RateLimit-") and header_name.endswith("-Reset"):
                # Extract dimension name: X-RateLimit-{dimension}-Reset
                dimension = header_name[12:-6]  # Remove 'X-RateLimit-' and '-Reset'
                available_dimensions.append(dimension)

        # For orders/trading endpoints, prioritize trade-related dimensions
        if "/orders" in url or "/trade/" in url:
            # Look for trade/order specific dimensions first
            for dim in available_dimensions:
                if any(keyword in dim.lower() for keyword in ["trade", "order", "post"]):
                    return dim

            # Fallback to Session if available
            if "Session" in available_dimensions:
                return "Session"

        # For other endpoints, prefer Session if available
        elif any(high_freq_endpoint in url for high_freq_endpoint in ["/positions", "/balances", "/portfolio"]):
            if "Session" in available_dimensions:
                return "Session"

        # Return the first non-AppDay dimension if available
        for dim in available_dimensions:
            if dim != "AppDay":
                return dim

        # Last resort: if only AppDay is available, we'll handle this in the fallback logic
        if "AppDay" in available_dimensions:
            return "AppDay"

        # If no headers are available at all, default to Session
        return "Session"

    def __request(
        self,
        method: str,
        url: str,
        request_args: dict[str, Any],
        headers: dict[str, str] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        """__request.

        make the actual request. This method is called by the
        request method in case of 'regular' API-calls. Or indirectly by
        the __stream_request method if it concerns a 'streaming' call.
        """
        func = getattr(self.client, method)
        headers = headers if headers else {}
        response = None

        # Check rate limits before making the request
        self.rate_limiter.wait_if_needed()

        logger.info("performing (%s) request %s", method, url)
        try:
            response = func(url, stream=stream, headers=headers, **request_args)
            # Update rate limits from response headers
            self.rate_limiter.update_limits(response.headers)
        except requests.RequestException as err:
            logger.error("request %s failed [%s]", url, err)
            raise err

        # Handle rate limit errors specifically
        if response.status_code == 429:
            # First, log ALL rate limit related headers for debugging
            all_rate_limit_headers = {}
            for header_name, header_value in response.headers.items():
                if "rate" in header_name.lower() or "limit" in header_name.lower():
                    all_rate_limit_headers[header_name] = header_value

            logger.warning(f"Rate limit exceeded (429). All rate limit headers: {all_rate_limit_headers}")

            # Detect which dimension actually caused the rate limit
            limiting_dimension = self._detect_limiting_dimension(response.headers, url)

            # Get the reset time for the limiting dimension
            wait_time = 0
            reset_info = []

            # Dynamically process all available reset headers
            for header_name, header_value in response.headers.items():
                if header_name.startswith("X-RateLimit-") and header_name.endswith("-Reset"):
                    # Extract dimension name: X-RateLimit-{dimension}-Reset
                    dimension = header_name[12:-6]  # Remove 'X-RateLimit-' and '-Reset'
                    reset_time = int(header_value)
                    reset_info.append(f"{dimension}:{reset_time}s")

                    # Use the reset time of the limiting dimension
                    if dimension == limiting_dimension:
                        # Special handling for Reset=0 or very small values
                        if reset_time == 0:
                            wait_time = 2  # 2 second wait for immediate reset
                            limiting_dimension = f"{dimension} (immediate reset, 2s wait)"
                            logger.info(f"{dimension} limit with immediate reset (0s), using short wait of {wait_time}s")
                        elif reset_time <= 10:
                            wait_time = reset_time + 1  # Add 1 second margin for short resets
                            limiting_dimension = f"{dimension} (short reset + 1s margin)"
                            logger.info(f"{dimension} limit with short reset time ({reset_time}s), using {wait_time}s with safety margin")
                        elif dimension == "AppDay" and reset_time > 300:  # More than 5 minutes
                            wait_time = 60  # Use 1 minute default for long AppDay resets
                            limiting_dimension = "AppDay (using default 60s)"
                            logger.info(f"AppDay limit detected with long reset time ({reset_time}s), using reasonable default of {wait_time}s instead")
                        else:
                            wait_time = reset_time

            # Fallback strategy if limiting dimension couldn't be determined
            if wait_time == 0:
                if reset_info:
                    # Smart fallback: don't wait for AppDay unless it's the only reasonable option
                    all_reset_times = []
                    non_appday_times = []

                    for info in reset_info:
                        dimension_name = info.split(":")[0]
                        time_str = info.split(":")[1].rstrip("s")
                        reset_time = int(time_str)
                        all_reset_times.append(reset_time)

                        # Collect non-AppDay reset times
                        if dimension_name != "AppDay":
                            non_appday_times.append(reset_time)

                    # If we only have AppDay reset time, use a reasonable default instead
                    if len(reset_info) == 1 and reset_info[0].startswith("AppDay:"):
                        wait_time = 60  # Default 1-minute wait instead of hours
                        limiting_dimension = "AppDay (using default 60s)"
                        logger.info(f"Only AppDay limit available ({all_reset_times[0]}s), using reasonable default of {wait_time}s instead")

                    # If we have non-AppDay times, use the minimum of those
                    elif non_appday_times:
                        wait_time = min(non_appday_times)
                        limiting_dimension = "Unknown (using minimum non-AppDay)"

                    # Otherwise use minimum of all (but this should rarely happen)
                    else:
                        wait_time = min(all_reset_times)
                        limiting_dimension = "Unknown (using minimum)"
                else:
                    # No reset headers found, use default
                    wait_time = 60
                    reset_info = ["Default:60s"]
                    limiting_dimension = "Default"

            logger.warning(f"Rate limit exceeded (429) for dimension: {limiting_dimension}. Reset times: {', '.join(reset_info)}. Waiting {wait_time} seconds")
            time.sleep(wait_time)

            # Update rate limits from response headers before retry
            self.rate_limiter.update_limits(response.headers)

            # Retry the request once after waiting
            response = func(url, stream=stream, headers=headers, **request_args)

        # Handle other error responses
        if response.status_code >= 400:
            logger.error(
                "request %s failed [%d,%s]",
                url,
                response.status_code,
                response.content.decode("utf-8"),
            )
            raise OpenAPIError(response.status_code, response.reason, response.content.decode("utf-8"))
        return response

    def __stream_request(
        self,
        method: str,
        url: str,
        request_args: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Iterator[Any]:
        """__stream_request.

        make a 'stream' request. This method is called by
        the 'request' method after it has determined which
        call applies: regular or streaming.
        """
        headers = headers if headers else {}
        response = self.__request(method, url, request_args, headers=headers, stream=True)
        lines = response.iter_lines(ITER_LINES_CHUNKSIZE)
        for line in lines:
            if line:
                data = json.loads(line.decode("utf-8"))
                yield data

    def request(self, endpoint: Any) -> Any:
        """Perform a request for the APIRequest instance 'endpoint'.

        Parameters
        ----------
        endpoint : APIRequest
            The endpoint parameter contains an instance of an APIRequest
            containing the endpoint, method and optionally other parameters
            or body data.

        Raises
        ------
            OpenAPIError in case of HTTP response code >= 400
        """
        method = endpoint.method
        method = method.lower()
        params = None
        try:
            params = endpoint.params
        except AttributeError:
            # request does not have params
            params = {}

        headers = {}
        if hasattr(endpoint, "HEADERS"):
            headers = endpoint.HEADERS

        request_args = {}

        if method in ["get", "delete", "patch"]:
            request_args["params"] = params

        if hasattr(endpoint, "data") and endpoint.data:
            request_args["json"] = endpoint.data

        # if any parameter for request then merge them
        request_args.update(self._request_params)

        # which API to access ?
        if not (hasattr(endpoint, "STREAM") and endpoint.STREAM is True):
            url = mk_endpoint(endpoint, self.environment, "api")

            response = self.__request(method, url, request_args, headers=headers)
            if hasattr(endpoint, "RESPONSE_DATA") and endpoint.RESPONSE_DATA is None:
                content = None

            elif not (hasattr(endpoint, "RESPONSE_DATA") and endpoint.RESPONSE_DATA == "text"):
                # if not explicitely set to 'text' asume JSON
                content = response.content.decode("utf-8")
                content = json.loads(content)

            else:
                content = response.content.decode("utf-8")

            # update endpoint
            endpoint.response = content
            endpoint.status_code = response.status_code

            return content

        else:
            url = mk_endpoint(endpoint, self.environment, "stream")
            endpoint.response = self.__stream_request(method, url, request_args, headers=headers)
            return endpoint.response

    def update_access_token(self, new_token: str) -> bool:
        """アクセストークンを更新し、HTTPヘッダーを更新する

        Args:
            new_token: 新しいアクセストークン

        Returns:
            bool: 更新成功かどうか
        """
        try:
            self.access_token = new_token
            self.client.headers["Authorization"] = "Bearer " + new_token
            logger.info("Access token updated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to update access token: {e}")
            return False

    def get_token_info(self) -> dict:
        """現在のトークン情報を返却する

        Returns:
            dict: トークン情報（期限等）
        """
        try:
            # JWT トークンをデコードして期限情報を取得
            import base64
            import json
            from datetime import datetime

            if not hasattr(self, "access_token") or not self.access_token:
                return {"valid": False, "error": "No access token available"}

            # JWTの構造: header.payload.signature
            token_parts = self.access_token.split(".")
            if len(token_parts) != 3:
                return {"valid": False, "error": "Invalid token format"}

            # payloadをデコード（padding調整）
            payload = token_parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding

            decoded_payload = base64.urlsafe_b64decode(payload)
            claims = json.loads(decoded_payload.decode("utf-8"))

            current_time = int(time.time())
            exp_time = int(claims.get("exp", 0))

            return {
                "valid": current_time < exp_time,
                "expires_at": exp_time,
                "expires_at_readable": datetime.fromtimestamp(exp_time).strftime("%Y-%m-%d %H:%M:%S"),
                "time_to_expiry": max(0, exp_time - current_time),
                "client_key": claims.get("cid"),
                "session_id": claims.get("sid"),
            }
        except Exception as e:
            logger.error(f"Failed to get token info: {e}")
            return {"valid": False, "error": str(e)}

    def reauthorize_streaming_context(self, context_id: str) -> bool:
        """WebSocketストリーミング接続の再認証を実行する

        Args:
            context_id: WebSocketのコンテキストID

        Returns:
            bool: 再認証成功かどうか
        """
        try:
            logger.info(f"Attempting to reauthorize streaming context: {context_id}")

            # ベースURLの構築
            base_url = TRADING_ENVIRONMENTS[self.environment]["stream"]
            path = "streamingws/authorize"

            if self.environment == "simulation":
                url = f"{base_url}/sim/openapi/{path}?contextid={context_id}"
            else:
                url = f"{base_url}/openapi/{path}?contextid={context_id}"

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }

            response = requests.put(url, headers=headers, timeout=10)

            if response.status_code == 202:
                logger.info(f"Successfully reauthorized streaming context: {context_id}")
                return True
            else:
                logger.error(f"Failed to reauthorize streaming context. Status: {response.status_code}, Response: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error during streaming context reauthorization: {e}")
            return False
