#!/usr/bin/env python3

"""Portfolio FX API Verification Sample

This script demonstrates fetching FX-related portfolio data:
- GET /port/v1/balances/me - Account balances
- GET /port/v1/positions/me - Current positions (including FX)
- GET /port/v1/orders/me - Open orders

The script is designed to:
1. Load SAXO_24H_TOKEN from .env
2. Authenticate with Saxo Bank API
3. Fetch balance, position, and order data
4. Handle errors gracefully (network, API limits)
5. Output results to stdout in JSON format

This is a verification sample script for operational validation. It outputs results
as a JSON object with the following structure:
  - status: Overall result status (success, partial_failure, failure)
  - timestamp: ISO 8601 timestamp of script execution
  - balances: API response data or None
  - positions: API response data or None
  - orders: API response data or None
  - errors: List of error messages encountered

Usage:
    uv run python libs/saxo_openapi/samples/verify_portfolio_fx.py

Requirements:
    - .env file with SAXO_24H_TOKEN environment variable
    - saxo_openapi library installed
    - Network connectivity to Saxo Bank API
"""

import json
import logging
import os
import sys
from datetime import UTC, datetime
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
    from saxo_openapi.endpoints.portfolio import balances, orders, positions
except ImportError as e:
    logger.error("Failed to import saxo_openapi: %s", str(e))
    logger.error("Please ensure saxo_openapi is installed: uv add saxo-openapi")
    sys.exit(1)


def main() -> int:
    """
    Main function for Portfolio FX verification.

    Returns:
        int: Exit code (0 for success, 1 for failure)
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
        "timestamp": datetime.now(UTC).isoformat(),
        "balances": None,
        "positions": None,
        "orders": None,
        "errors": [],
    }

    # Fetch account balances
    try:
        logger.info("Fetching account balances...")
        balances_request = balances.AccountBalancesMe()
        client.request(balances_request)
        results["balances"] = balances_request.response
        logger.info("Balances fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching balances - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error fetching balances - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching balances: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Fetch current positions
    try:
        logger.info("Fetching current positions...")
        positions_request = positions.PositionsMe()
        client.request(positions_request)
        results["positions"] = positions_request.response
        logger.info("Positions fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching positions - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error fetching positions - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching positions: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Fetch open orders
    try:
        logger.info("Fetching open orders...")
        orders_request = orders.GetOpenOrdersMe()
        client.request(orders_request)
        results["orders"] = orders_request.response
        logger.info("Orders fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching orders - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error fetching orders - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching orders: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Determine overall status
    if results["errors"]:
        # A call is considered successful if it produced a response (is not None)
        has_successful_response = results["balances"] is not None or results["positions"] is not None or results["orders"] is not None
        results["status"] = "partial_failure" if has_successful_response else "failure"

    # Output results to stdout
    print(json.dumps(results, indent=2))

    # Return exit code based on status
    return 0 if not results["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
