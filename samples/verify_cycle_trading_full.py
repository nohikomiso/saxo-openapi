#! /usr/bin/env python3
"""
Full Trading Cycle Verification Sample (Market Order)

This sample demonstrates a complete trading cycle with execution:
1. Setup: Place a Market Buy order (Instant execution)
2. Verify: Confirm Position creation
3. Close: Place a Market Close order (Exclusive Close)
4. Teardown: Verify Position is closed

WARNING: This executes a MARKET ORDER which will trade immediately.
Use only in Simulation/Demo environment.

Usage:
    uv run libs/saxo_openapi/samples/verify_cycle_trading_full.py
"""

import json
import logging
import os
import sys
import time

import saxo_openapi.endpoints.portfolio as pf
import saxo_openapi.endpoints.trading as tr
from dotenv import load_dotenv
from saxo_openapi import API
from saxo_openapi.contrib.orders import MarketOrderFxSpot, tie_account_to_order

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    if not token:
        logger.error("Error: SAXO_24H_TOKEN not found in .env")
        sys.exit(1)

    client = API(access_token=token)

    try:
        # 1. Setup: Get AccountKey
        logger.info("Step 1: Fetching AccountKey...")
        r_accounts = pf.accounts.AccountsMe()
        client.request(r_accounts)
        account_key = r_accounts.response["Data"][0]["AccountKey"]
        client_key = r_accounts.response["Data"][0]["ClientKey"]
        logger.info(f"AccountKey: {account_key}")

        # 2. Open Position: Place a Market Buy order for USDJPY (Uic 42)
        logger.info("Step 2: Opening a Long position for USDJPY (Market Order)...")
        mo = MarketOrderFxSpot(
            Uic=42,
            Amount=10000,
            ExternalReference="full_cycle_test_open"
        )
        order_data = tie_account_to_order(account_key, mo)
        r_order = tr.orders.Order(data=order_data)
        client.request(r_order)
        order_id = r_order.response["OrderId"]
        logger.info(f"Open order placed. OrderId: {order_id}")

        # 3. Wait and Verify Position
        logger.info("Step 3: Waiting for position to be created...")
        position_id = None
        for i in range(10):  # Try for 10 seconds
            time.sleep(1)
            r_positions = pf.positions.PositionsMe()
            client.request(r_positions)
            
            # Find position for Uic 42
            for pos in r_positions.response.get("Data", []):
                if pos["PositionBase"]["Uic"] == 42:
                    position_id = pos["PositionId"]
                    logger.info(f"Position found! PositionId: {position_id}")
                    break
            if position_id:
                break
        
        if not position_id:
            logger.error("Failed to find the opened position.")
            return

        # 4. Close Position: Place a Market Close order (Exclusive Close)
        logger.info(f"Step 4: Closing position {position_id} (Market Close Order)...")
        
        # Use the new utility class MarketCloseOrder
        # This handles the complex structure of explicit position closure
        # (PositionId at top level + nested Orders list)
        
        # NOTE: In a real application, you should check Netting Mode here.
        # if netting_mode == 'FifoEndOfDay': use MarketCloseOrder (Exclusive Close)
        # if netting_mode == 'FifoRealTime': usage depends on API version/config
        
        from saxo_openapi.contrib.orders import MarketCloseOrder
        
        close_order = MarketCloseOrder(
            PositionId=position_id,
            Uic=42,
            Amount=10000,
            AssetType='FxSpot',
            BuySell='Sell', # Explicitly selling to close Long
            OrderType='Market',
            ManualOrder=True 
        )
        
        # Inject AccountKey - tie_account_to_order handles the logic correctly for MarketCloseOrder
        # (injecting into nested Orders list instead of top level)
        close_order_data = tie_account_to_order(account_key, close_order)
        
        logger.info(f"Close Order Data (Utility): {json.dumps(close_order_data, indent=2)}")
        
        r_close = tr.orders.Order(data=close_order_data)
        client.request(r_close)
        
        # Handle nested response structure
        if "Orders" in r_close.response and isinstance(r_close.response["Orders"], list):
             close_order_id = r_close.response["Orders"][0]["OrderId"]
        else:
             close_order_id = r_close.response["OrderId"]
             
        logger.info(f"Close order placed. OrderId: {close_order_id}")

        # 5. Final Verification: Check if position is gone
        logger.info("Step 5: Verifying position closure...")
        time.sleep(2)
        r_positions_final = pf.positions.PositionsMe()
        client.request(r_positions_final)
        
        still_exists = False
        for pos in r_positions_final.response.get("Data", []):
            if pos["PositionId"] == position_id:
                still_exists = True
                break
        
        if still_exists:
            logger.error(f"Position {position_id} still exists after close order.")
        else:
            logger.info(f"Position {position_id} has been successfully closed.")

        result = {
            "status": "success" if not still_exists else "failed",
            "open_order_id": order_id,
            "position_id": position_id,
            "close_order_id": close_order_id,
            "final_status": "Closed" if not still_exists else "Still Open"
        }
        print(json.dumps(result, indent=2))

    except Exception as e:
        logger.error(f"Verification Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
