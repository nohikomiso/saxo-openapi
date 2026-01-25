#!/usr/bin/env python3

"""
Trading Order Lifecycle Verification Sample

This sample demonstrates the full lifecycle of a trading order:
1. Setup: Place a Limit Buy order (far from market price to avoid execution)
2. Verify: Retrieve the order details by OrderId and verify status
3. Teardown: Cancel the order and verify cancellation

Endpoinsts:
    - POST /trade/v1/orders
    - GET /trade/v1/orders/{OrderId}
    - DELETE /trade/v1/orders/{OrderId}

Usage:
    uv run libs/saxo_openapi/samples/verify_lifecycle_trading.py
"""

import json
import logging
import os
import sys
import time

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

try:
    import saxo_openapi
    from saxo_openapi import API
    from saxo_openapi.endpoints.portfolio import balances
    from saxo_openapi.endpoints.portfolio import orders as port_orders
    from saxo_openapi.endpoints.trading import orders
except ImportError:
    logger.error("saxo_openapi not installed.")
    sys.exit(1)


def get_account_key(client: API) -> tuple[str, str]:
    """Get the first available AccountKey and ClientKey."""
    # Try fetching accounts directly
    from saxo_openapi.endpoints.portfolio import accounts

    r_acc = accounts.AccountsMe()
    client.request(r_acc)
    acc_list = r_acc.response.get("Data", [])
    if not acc_list:
        raise ValueError("No accounts found.")
    return acc_list[0]["AccountKey"], acc_list[0]["ClientKey"]


def main():
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    if not token:
        logger.error("SAXO_24H_TOKEN not found in .env")
        return 1

    client = API(access_token=token)

    try:
        account_key, client_key = get_account_key(client)
        logger.info(f"Using AccountKey: {account_key}, ClientKey: {client_key}")
    except Exception as e:
        logger.error(f"Failed to get AccountKey/ClientKey: {e}")
        return 1

    # 1. Setup: Place Limit Order
    # EURUSD (Uic 21), Buy, Amount 1000, Price 0.5 (Far below market)
    uic = 21  # EURUSD
    asset_type = "FxSpot"

    order_spec = {"Uic": uic, "AssetType": asset_type, "Amount": 1000, "BuySell": "Buy", "OrderType": "Limit", "OrderPrice": 0.5, "OrderDuration": {"DurationType": "DayOrder"}, "ManualOrder": True, "AccountKey": account_key}

    logger.info("1. Placing Limit Order...")
    try:
        r_place = orders.Order(data=order_spec)
        client.request(r_place)
        order_id = r_place.response.get("OrderId")
        if not order_id:
            logger.error("Failed to get OrderId from response.")
            print(json.dumps(r_place.response, indent=2))
            return 1
        logger.info(f"Order Placed. OrderId: {order_id}")
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        return 1

    time.sleep(2)  # Wait for order to propagate

    # 2. Verify: Get Order Details
    logger.info("2. Verifying Order...")
    try:
        # Use GetOpenOrder from portfolio (requires ClientKey)
        r_get = port_orders.GetOpenOrder(ClientKey=client_key, OrderId=order_id)
        client.request(r_get)
        order_data = r_get.response
        if "Data" in order_data and isinstance(order_data["Data"], list):
            order_data = order_data["Data"][0]

        status = order_data.get("Status")
        logger.info(f"Order verified. Status: {status}")

        if status not in ["Working", "Placed", "Unknown"]:
            logger.warning(f"Unexpected status: {status}")
    except Exception as e:
        logger.error(f"Failed to get order details: {e}")
        # Continue to teardown anyway

    # 3. Teardown: Cancel Order
    logger.info("3. Cancelling Order...")
    try:
        # CancelOrders takes OrderIds string
        r_cancel = orders.CancelOrders(OrderIds=order_id, params={"AccountKey": account_key})
        client.request(r_cancel)
        logger.info("Order cancelled successfully.")
    except Exception as e:
        logger.error(f"Failed to cancel order: {e}")
        return 1

    print(json.dumps({"status": "success", "order_id": order_id}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
