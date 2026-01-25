#!/usr/bin/env python3

"""ReferenceData FX API Verification Sample

This script demonstrates fetching FX-related reference data:
- GET /ref/v1/currencies - Available currencies (FX base)
- GET /ref/v1/currencypairs - Currency pairs (FX major/minor)
- GET /ref/v1/instruments - Instrument list with optional search parameters (FX lookup)

The script is designed to:
1. Load SAXO_24H_TOKEN from .env
2. Authenticate with Saxo Bank API
3. Fetch currency, currency pair, and instrument data
4. Handle errors gracefully (network, API limits)
5. Output results to stdout in JSON format

This is a verification sample script for operational validation. It outputs results
as a JSON object with the following structure:
  - status: Overall result status (success, partial_failure, failure)
  - timestamp: ISO 8601 timestamp of script execution
  - currencies: API response data or None
  - currency_pairs: API response data or None
  - instruments: API response data or None
  - errors: List of error messages encountered

Usage:
    uv run python libs/saxo_openapi/samples/verify_refdata_fx.py

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
    from saxo_openapi.endpoints.referencedata import (
        currencies,
        currencypairs,
        instruments,
    )
except ImportError as e:
    logger.error("Failed to import saxo_openapi: %s", str(e))
    logger.error("Please ensure saxo_openapi is installed: uv add saxo-openapi")
    sys.exit(1)


def main() -> int:
    """
    Main function for ReferenceData FX verification.

    Fetches FX reference data from Saxo Bank API and outputs results as JSON.
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
        "timestamp": datetime.now(UTC).isoformat(),
        "currencies": None,
        "currency_pairs": None,
        "instruments": None,
        "errors": [],
    }

    # Fetch available currencies
    try:
        logger.info("Fetching available currencies...")
        currencies_request = currencies.Currencies()
        client.request(currencies_request)
        results["currencies"] = currencies_request.response
        logger.info("Currencies fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching currencies - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error fetching currencies - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching currencies: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Fetch currency pairs
    try:
        logger.info("Fetching currency pairs...")
        pairs_request = currencypairs.CurrencyPairs()
        client.request(pairs_request)
        results["currency_pairs"] = pairs_request.response
        logger.info("Currency pairs fetched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error fetching currency pairs - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error fetching currency pairs - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching currency pairs: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Search for instruments (using FX as search term)
    try:
        logger.info("Searching for FX instruments...")
        search_request = instruments.Instruments(params={"keywords": "EUR", "assetTypes": "FxSpot"})
        client.request(search_request)
        results["instruments"] = search_request.response
        logger.info("Instruments searched successfully")
    except (ConnectionError, TimeoutError) as e:
        error_msg = f"Network error searching instruments - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify network connectivity to Saxo Bank API")
        results["errors"].append(error_msg)
    except ValueError as e:
        error_msg = f"API request error searching instruments - {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.error("Please verify API parameters and request format")
        results["errors"].append(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error searching instruments: {str(e)}"
        logger.error(error_msg, exc_info=True)
        results["errors"].append(error_msg)

    # Determine overall status based on errors
    # If errors occurred, check if at least one API call succeeded
    if results["errors"]:
        # A call is considered successful if it produced a response (is not None)
        has_successful_response = results["currencies"] is not None or results["currency_pairs"] is not None or results["instruments"] is not None
        # Set status: partial_failure if some calls succeeded, failure if all failed
        results["status"] = "partial_failure" if has_successful_response else "failure"

    # Output results to stdout in JSON format for parsing by external tools/scripts
    print(json.dumps(results, indent=2))

    # Return exit code based on status
    return 0 if not results["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
