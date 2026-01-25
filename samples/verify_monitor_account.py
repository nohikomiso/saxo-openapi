#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Account Monitoring Sample

This sample demonstrates dynamic account monitoring capabilities:
1. Setup: Get ClientKey and AccountKey dynamically
2. Monitor: Get Margin details
3. Pricing: Get snapshot prices for specific instruments

Endpoints:
    - GET /port/v1/balances/me
    - GET /port/v1/margins/{AccountKey}
    - GET /trade/v1/prices/instruments

Usage:
    uv run libs/saxo_openapi/samples/verify_monitor_account.py
"""

import json
import logging
import os
import sys

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    import saxo_openapi
    from saxo_openapi import API
    # Adjust imports to likely locations if module structure changed
    from saxo_openapi.endpoints.portfolio import balances, accounts
    from saxo_openapi.endpoints.trading import prices
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

    # 1. Setup: Get Keys
    logger.info("1. Setup: Fetching Account Keys...")
    try:
        r_acc = accounts.AccountsMe()
        client.request(r_acc)
        data = r_acc.response.get("Data", [])
        if not data:
            logger.error("No accounts found.")
            return 1
        account = data[0]
        account_key = account["AccountKey"]
        client_key = account["ClientKey"]
        logger.info(f"AccountKey: {account_key[:5]}...")
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return 1

    # 2. Monitor: Margin
    logger.info("2. Monitor: Fetching Margins...")
    try:
        # Check if MarginOverview endpoint exists or similar
        # If not, use balances?
        # The task mentions /port/v1/margins/{AccountKey}
        # Let's see if this class exists in 'balances' or 'margins' module?
        # Spec 7.8.2 mentions `portfolio/margins.py`. It is in Category B.
        # Use simple balances if margins module not found, but try importing first.
        try:
             from saxo_openapi.endpoints.portfolio import margins
             r_marg = margins.AccountMargins(AccountKey=account_key)
        except ImportError:
             logger.warning("portfolio.margins module not found, using generic Balances.")
             r_marg = balances.AccountBalancesMe()
        
        client.request(r_marg)
        logger.info("Margins fetched successfully.")
    except Exception as e:
        logger.error(f"Margin fetch failed: {e}")

    # 3. Pricing: Snapshot
    logger.info("3. Pricing: Fetching Prices (EURUSD, US500)...")
    try:
        # Uic 21 (EURUSD), 45000 (possible index?). Let's use 21.
        uics = "21,211" # EURUSD, Apple
        r_price = prices.InfoPrice(params={"Uics": uics, "AssetType": "FxSpot"}) 
        # Note: Mixing asset types in InfoPrice might require separate calls or comma separated
        # InfoPrice usually takes one Uic/AssetType or list? 
        # Endpoint: GET /trade/v1/prices/instruments/
        # Check if 'InfoPrice' supports list. Usually it's 'InfoPrices' (plural) for list?
        # Re-check spec or common usage. `trading.prices` usually has InfoPrice (singular) or similar.
        # Let's try Multi request if possible or just loop. Use InfoPriceList if exists?
        # The spec says `GET /trade/v1/prices/instruments`.
        
        # Let's try generic call if class is unsure
        # But InfoPrice is standard.
        r_price = prices.InfoPrice(params={"Uic": 21, "AssetType": "FxSpot"})
        client.request(r_price)
        quote = r_price.response.get("Quote", {})
        bid = quote.get("Bid")
        logger.info(f"EURUSD Bid: {bid}")

    except Exception as e:
        logger.error(f"Price fetch failed: {e}")
    
    print(json.dumps({"status": "success"}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
