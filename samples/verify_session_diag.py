#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""Session and Diagnostics API Verification Sample

This script demonstrates checking API connection and server status:
- GET /root/v1/sessions/capabilities - Session information, user profile, and account capabilities
- GET /root/v1/diagnostics - Server diagnostics including version, latency, and status

The script is designed to:
1. Load SAXO_24H_TOKEN from .env
2. Authenticate with Saxo Bank API
3. Fetch session capabilities and status
4. Check API connectivity and operational status
5. Verify session validity and permissions
6. Handle errors gracefully (network, API limits)
7. Output results to stdout in JSON format

This is a verification sample script for operational validation. It outputs results
as a JSON object with the following structure:
  - status: Overall result status (success, partial_failure, failure)
  - timestamp: ISO 8601 timestamp of script execution
  - session_capabilities: API response data or None
  - diagnostics: API response data or None
  - api_connectivity: Connection status indicator (success, failed, unknown)
  - errors: List of error messages encountered

Usage:
    uv run python libs/saxo_openapi/samples/verify_session_diag.py

Requirements:
    - .env file with SAXO_24H_TOKEN environment variable
    - saxo_openapi library installed
    - Network connectivity to Saxo Bank API
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv

# Configure logging for better error reporting
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)

logger = logging.getLogger(__name__)

try:
    import saxo_openapi
    from saxo_openapi.endpoints.rootservices import diagnostics, sessions
except ImportError as e:
    logger.error("Failed to import saxo_openapi: %s", str(e))
    logger.error("Please ensure saxo_openapi is installed: uv add saxo-openapi")
    sys.exit(1)


def main() -> int:
    """
    Main function for Session and Diagnostics verification.

    Fetches session capabilities and diagnostics from Saxo Bank API and outputs results as JSON.
    This is a verification sample script for operational validation.

    Environment:
        SAXO_24H_TOKEN: Required. Authentication token from .env file

    Returns:
        int: Exit code (0 for success with no errors, 1 if any errors occurred)
    """
    # Load environment variables
    load_dotenv()

    # Get authentication token
    token = os.getenv("SAXO_24H_TOKEN")
    if not token:
        logger.error("SAXO_24H_TOKEN not found in .env file")
        logger.error("Please set SAXO_24H_TOKEN in your .env file")
        return 1

    # Initialize API client
    try:
        client = saxo_openapi.API(access_token=token)
    except ValueError as e:
        logger.error("Authentication failed - Invalid token: %s", str(e))
        logger.error("Please verify SAXO_24H_TOKEN is valid and not expired")
        return 1
    except Exception as e:
        logger.error("Failed to initialize API client: %s", str(e))
        return 1

    # Container for results
    results: dict[str, Any] = {
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_capabilities": None,
        "diagnostics": None,
        "api_connectivity": "unknown",
        "errors": [],
    }

    # Fetch session capabilities
    try:
        logger.info("Fetching session capabilities...")
        session_request = sessions.GetSessionCapabilities()
        client.request(session_request)
        results["session_capabilities"] = session_request.response
        results["api_connectivity"] = "success"
        logger.info("Session capabilities fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching session capabilities - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
        results["api_connectivity"] = "failed"
    except ValueError as e:
        error_msg = f"API request error fetching session capabilities - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
        results["api_connectivity"] = "failed"
    except Exception as e:
        error_msg = f"Unexpected error fetching session capabilities: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)
        results["api_connectivity"] = "failed"

    # Fetch diagnostics (using GET endpoint for health check)
    try:
        logger.info("Fetching server diagnostics...")
        diag_request = diagnostics.Get()
        client.request(diag_request)
        results["diagnostics"] = diag_request.response
        logger.info("Diagnostics fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching diagnostics - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = (
            f"API request error fetching diagnostics - {type(e).__name__}: {str(e)}"
        )
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching diagnostics: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Determine overall status based on errors
    # If errors occurred, check if at least one API call succeeded
    if results["errors"]:
        # A call is considered successful if it produced a response (is not None)
        has_successful_response = (
            results["session_capabilities"] is not None
            or results["diagnostics"] is not None
        )
        # Set status: partial_failure if some calls succeeded, failure if all failed
        results["status"] = "partial_failure" if has_successful_response else "failure"

    # Output results to stdout in JSON format for parsing by external tools/scripts
    print(json.dumps(results, indent=2))

    # Return exit code based on status
    return 0 if not results["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
