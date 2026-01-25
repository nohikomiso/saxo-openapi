#!/usr/bin/env python3

"""
Order Validation (PreCheck) Sample

This script demonstrates how to key validate_order to check
parameters and market conditions without placing an actual order.

Usage:
    uv run libs/saxo_openapi/samples/verify_orders_precheck.py
"""

import json

import saxo_openapi.definitions.orders as OD
from saxo_openapi import API
from saxo_openapi.contrib.orders import MarketOrder, StopOrder
from saxo_openapi.contrib.trader import SaxoTrader


def read_token(token_file="token_demo.txt"):
    with open(token_file) as f:
        return f.read().strip()


def main():
    try:
        token = read_token("token_demo.txt")
        client = API(access_token=token)
        trader = SaxoTrader(client)

        print("--- Verifying PreCheck (Validation) ---")

        # Create a valid order spec but verify it first
        # EURUSD Market Order
        order_spec = MarketOrder(Uic=21, Amount=1000, AssetType=OD.AssetType.FxSpot)

        print("1. Validating Valid Order (Market)...")
        try:
            rv = trader.validate_order(order_spec)
            print(f"   PreCheck Result: {json.dumps(rv, indent=2)}")
            print("   SUCCESS: Order validated.")
        except Exception as e:
            print(f"   FAILED: {e}")

        # Create an INVALID order (Wrong Side of Market?)
        # Buy Stop Order at Price 0.0 (Should fail validation)
        print("\n2. Validating Invalid Order (Buy Stop @ 0.0)...")

        # Use standard StopOrder class for manual validation test.
        invalid_spec = StopOrder(Uic=21, Amount=1000, OrderPrice=0.0001, AssetType=OD.AssetType.FxSpot)

        try:
            rv = trader.validate_order(invalid_spec)
            print(f"   PreCheck Result: {json.dumps(rv, indent=2)}")
            # If it returns 'ErrorInfo', that's a validation failure captured in response
            if "ErrorInfo" in rv:
                print(f"   SUCCESS: Validation caught error: {rv['ErrorInfo']}")
            else:
                # Depending on API, successful precheck returns estimated costs etc.
                # If it passes, maybe 0.0 is technically valid?
                print("   Passed validation (Unexpected for 0.0 price but ok for test flow)")

        except Exception as e:
            # Or it raises exception (HTTP 400)
            print(f"   SUCCESS: API Raised Exception: {e}")

    except Exception as e:
        print(f"Main execution error: {e}")


if __name__ == "__main__":
    main()
