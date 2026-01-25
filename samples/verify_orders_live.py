#!/usr/bin/env python3

"""
Live Order Verification Sample

This script demonstrates valid order placement using SaxoTrader:
- Limit Orders
- Stop Orders (Smart Routing)
- Stop Limit Orders

Usage:
    uv run libs/saxo_openapi/samples/verify_orders_live.py
"""

import time

import saxo_openapi.definitions.orders as OD
import saxo_openapi.endpoints.trading as tr
from saxo_openapi import API
from saxo_openapi.contrib.trader import SaxoTrader


def read_token(token_file="token_demo.txt"):
    with open(token_file) as f:
        return f.read().strip()


def get_current_price(client, uic, asset_type):
    # Use InfoPrice to get current Bid/Ask
    # InfoPrice expects a dictionary 'params' with Uic and AssetType
    try:
        r = tr.infoprices.InfoPrice(params={"Uic": uic, "AssetType": asset_type})
        res = client.request(r)
        # Quote object
        quote = res.get("Quote", {})
        bid = quote.get("Bid")
        ask = quote.get("Ask")
        mid = (bid + ask) / 2 if bid and ask else None
        print(f"   [Market Data] {asset_type} (UIC {uic}): Bid={bid}, Ask={ask}, Mid={mid}")
        return mid if mid else 0.0
    except Exception as e:
        print(f"   [Market Data] Failed to fetch price: {e}")
        return 0.0


def place_orders(client, trader, name, uic, asset_type, default_price):
    print(f"\n=== Testing {name} (UIC: {uic}, Asset: {asset_type}) ===")

    # Fetch live price
    current_price = get_current_price(client, uic, asset_type)
    if current_price == 0.0:
        print(f"   Using default price estimate: {default_price}")
        current_price = default_price

    # 1. Limit Order (指値) - Buy Limit Below Market
    # 5% below for plenty buffer
    limit_price = current_price * 0.95
    if asset_type == "FxSpot":
        limit_price = current_price - 0.0050
    limit_price = round(limit_price, 4 if asset_type == "FxSpot" else 2)

    print(f"1. Placing Limit Order (Buy @ {limit_price})...")
    try:
        r = trader.limit_order(
            Uic=uic,
            Amount=1000 if asset_type == "FxSpot" else 1,
            OrderPrice=limit_price,
            AssetType=asset_type,
        )
        print(f"   SUCCESS: OrderId={r['OrderId']}")
    except Exception as e:
        print(f"   FAILED: {e}")

    time.sleep(1)  # Rate limit

    # 2. Stop Order (逆指値 -> 成行) - Buy Stop Above Market
    # 5% above for plenty buffer
    stop_price = current_price * 1.05
    if asset_type == "FxSpot":
        stop_price = current_price + 0.0050
    stop_price = round(stop_price, 4 if asset_type == "FxSpot" else 2)

    print(f"2. Placing Stop Order (Smart Routing, Buy Stop @ {stop_price})...")
    try:
        r = trader.stop_order(
            Uic=uic,
            Amount=1000 if asset_type == "FxSpot" else 1,
            OrderPrice=stop_price,
            AssetType=asset_type,
        )
        print(f"   SUCCESS: OrderId={r['OrderId']}")
    except Exception as e:
        print(f"   FAILED: {e}")

    time.sleep(1)  # Rate limit

    # 3. Stop Limit Order (逆指値 -> 指値) - Buy Stop Limit Above Market
    sl_trigger = stop_price
    sl_limit = stop_price * 1.01
    if asset_type == "FxSpot":
        sl_limit = stop_price + 0.0010
    sl_limit = round(sl_limit, 4 if asset_type == "FxSpot" else 2)

    print(f"3. Placing Stop Limit Order (Trigger @ {sl_trigger}, Limit @ {sl_limit})...")
    try:
        r = trader.stop_limit_order(
            Uic=uic,
            Amount=1000 if asset_type == "FxSpot" else 1,
            OrderPrice=sl_trigger,
            StopLimitPrice=sl_limit,
            AssetType=asset_type,
        )
        print(f"   SUCCESS: OrderId={r['OrderId']}")
    except Exception as e:
        print(f"   FAILED: {e}")

    time.sleep(1)  # Rate limit


def main():
    try:
        token = read_token("token_demo.txt")
        client = API(access_token=token)
        trader = SaxoTrader(client)

        # Ensure AccountKey is loaded
        print(f"AccountKey: {trader.account_key}")

        # --- FX Spot (EURUSD) ---
        place_orders(client, trader, "FX Spot (EURUSD)", 21, OD.AssetType.FxSpot, 1.05)

        # --- Stock (AAPL) ---
        place_orders(client, trader, "Stock (AAPL)", 211, OD.AssetType.Stock, 200.0)

        # --- CFD (AAPL) ---
        place_orders(client, trader, "CFD on Stock (AAPL)", 211, OD.AssetType.CfdOnStock, 200.0)

    except Exception as e:
        print(f"Main execution error: {e}")


if __name__ == "__main__":
    main()
