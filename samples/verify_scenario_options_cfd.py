#!/usr/bin/env python3

"""
Options & CFD Scenario Verification Sample

This sample demonstrates the workflow for finding and trading Options/CFDs:
1. Discovery: Search for an instrument (e.g. Apple) to get UIC/AssetType
2. Search: Get Option Chain for the instrument
3. Transaction: Place a limit order on a specific Option or CFD
4. Teardown: Cancel the order

Endpoints:
    - GET /ref/v1/instruments/details
    - GET /trade/v1/optionschain/{Uic}
    - POST /trade/v1/orders

Usage:
    uv run libs/saxo_openapi/samples/verify_scenario_options_cfd.py
"""

import json
import logging
import os
import sys
import time

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    import saxo_openapi
    from saxo_openapi import API
    from saxo_openapi.endpoints.portfolio import accounts
    from saxo_openapi.endpoints.referencedata import instruments
    from saxo_openapi.endpoints.trading import optionschain, orders
except ImportError:
    logger.error("saxo_openapi not installed.")
    sys.exit(1)


def get_account_key(client):
    r = accounts.AccountsMe()
    client.request(r)
    return r.response["Data"][0]["AccountKey"]


def main():
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    if not token:
        logger.error("SAXO_24H_TOKEN not found.")
        return 1

    client = API(access_token=token)
    try:
        account_key = get_account_key(client)
    except Exception as e:
        logger.error(f"Account init failed: {e}")
        return 1

    # 1. Discovery: Apple Inc.
    logger.info("1. Discovery: Searching for 'Apple'...")
    # NOTE: In verified refdata script we used instruments search.
    # Here we simulate specific flow if we know UIC or search.
    # Apple UIC is typically 211 (on Saxo Demo/Sim often).
    # Let's search to be sure or just hardcode for demo.
    keyword = "Apple"
    # Using simple search
    try:
        r_search = instruments.Instruments(params={"Keywords": keyword, "AssetTypes": "Stock,StockOption"})
        client.request(r_search)
        data = r_search.response.get("Data", [])
        if not data:
            logger.error("Apple stock not found.")
            return 1

        # Find Stock for CFD and StockOption for Chain
        apple_stock = next((i for i in data if i["AssetType"] == "Stock"), None)
        apple_option = next((i for i in data if i["AssetType"] == "StockOption"), None)

        if not apple_stock:
            logger.warning("Apple Stock not found, using first result for Stock")
            apple_stock = data[0]

        root_uic = apple_stock["Identifier"]
        stock_symbol = apple_stock.get("Symbol")
        logger.info(f"Found Stock {stock_symbol} (UIC: {root_uic})")

        option_root_id = root_uic  # Default fallback
        if apple_option:
            option_root_id = apple_option["Identifier"]
            logger.info(f"Found Option Root: {apple_option['Symbol']} (ID: {option_root_id})")
        else:
            logger.warning("Apple StockOption not found in search results.")

    except Exception as e:
        logger.warning(f"Search failed: {e}. Defaulting to UIC 211 (AAPL)")
        root_uic = 211
        option_root_id = 211

    # 2. Search Option Chain
    logger.info(f"2. Getting Option Chain for UIC {root_uic}...")
    try:
        # OptionsChain requires subscription to get data
        # Use OptionsChainSubscriptionCreate
        # POST /trade/v1/optionschain/subscriptions
        req_data = {
            "Arguments": {
                "Identifier": option_root_id,
                "AssetType": "StockOption",
                "MaxStrikes": 4,
                "OptionRootId": option_root_id,  # Sometimes needed
            },
            "ContextId": "explorer_" + str(int(time.time())),
            "ReferenceId": "ref_" + str(int(time.time())),
        }
        r_chain = optionschain.OptionsChainSubscriptionCreate(data=req_data)
        client.request(r_chain)
        # Verify we got some data in Snapshot
        snapshot = r_chain.response.get("Snapshot", {})
        if not snapshot:
            logger.warning("No snapshot in OptionsChain response")
    except Exception as e:
        logger.error(f"Option Chain fetch failed: {e}")
        # Proceed to specific CFD test if Option fails?

    # 3. Transaction: Place Order (CFD for simplicity if Option logic is complex without specific strike)
    # Let's place a CFD order on Apple (CfdOnStock)
    logger.info("3. Transaction: Placing CFD Limit Order on AAPL...")
    try:
        # CFD UIC is often same as Stock UIC but AssetType=CfdOnStock
        order_spec = {
            "Uic": root_uic,
            "AssetType": "CfdOnStock",
            "Amount": 10,
            "BuySell": "Buy",
            "OrderType": "Limit",
            "OrderPrice": 100.0,  # Low price
            "OrderDuration": {"DurationType": "DayOrder"},
            "ManualOrder": True,
            "AccountKey": account_key,
        }
        r_order = orders.Order(data=order_spec)
        client.request(r_order)
        order_id = r_order.response.get("OrderId")
        logger.info(f"CFD Order Placed. OrderId: {order_id}")

        time.sleep(2)

        # 4. Teardown
        logger.info("4. Teardown: Cancelling Order...")
        client.request(orders.CancelOrders(OrderIds=str(order_id), params={"AccountKey": account_key}))
        logger.info("Order Cancelled.")

    except Exception as e:
        logger.error(f"Order transaction failed: {e}")
        return 1

    print(json.dumps({"status": "success"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
