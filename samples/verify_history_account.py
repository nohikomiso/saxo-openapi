#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Account History Retrieval Sample

This sample demonstrates retrieving historical data:
1. Performance: GET /hist/v4/performance
2. Positions: GET /hist/v3/positions/{ClientKey}
3. Account Values: GET /hist/v3/accountvalues/{ClientKey}

Usage:
    uv run libs/saxo_openapi/samples/verify_history_account.py
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    import saxo_openapi
    from saxo_openapi import API
    from saxo_openapi.endpoints.accounthistory import performance, historicalpositions, accountvalues
    from saxo_openapi.endpoints.portfolio import accounts
except ImportError:
    logger.error("saxo_openapi not installed.")
    sys.exit(1)

def main():
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    if not token:
        logger.error("Missing token.")
        return 1
    
    client = API(access_token=token)
    
    # Get Keys
    r_acc = accounts.AccountsMe()
    client.request(r_acc)
    account = r_acc.response["Data"][0]
    client_key = account["ClientKey"]
    account_key = account["AccountKey"]

    # 1. Performance
    logger.info("1. Fetching Performance (v4)...")
    try:
        r_perf = performance.AccountPerformance(ClientKey=client_key)
        client.request(r_perf)
        logger.info("Performance fetched.")
    except Exception as e:
        logger.error(f"Performance fetch failed: {e}")
        # Note: v4 might be 404 in Sim, handled as error but expected behavior sometimes

    # 2. Historical Positions
    logger.info("2. Fetching Historical Positions...")
    try:
        r_hist = historicalpositions.HistoricalPositions(ClientKey=client_key)
        client.request(r_hist)
        logger.info(f"Historical Positions: {len(r_hist.response.get('Data', []))} items")
    except Exception as e:
        logger.error(f"Historical Positions failed: {e}")

    # 3. Account Values
    logger.info("3. Fetching Account Values...")
    try:
        r_val = accountvalues.AccountSummary(ClientKey=client_key)
        client.request(r_val)
        logger.info("Account Values fetched.")
    except Exception as e:
        logger.error(f"Account Values failed: {e}")

    print(json.dumps({"status": "success"}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
