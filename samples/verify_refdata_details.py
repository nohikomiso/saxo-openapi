#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Detailed Reference Data Verification Sample

Test comprehensive reference data:
- Instruments Details
- Exchanges
- Languages
- TimeZones

Usage:
    uv run libs/saxo_openapi/samples/verify_refdata_details.py
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
    from saxo_openapi.endpoints.referencedata import instruments, exchanges, languages, timezones
except ImportError:
    logger.error("Imports failed.")
    sys.exit(1)

def main():
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    if not token: 
        return 1
    client = API(access_token=token)

    # 1. Instrument Details (Apple Uic 211)
    logger.info("1. Instrument Details (UIC 211)...")
    try:
        # InstrumentsDetails takes Uics (plural) or specific params
        r_inst = instruments.InstrumentsDetails(Uics="211", AssetTypes="Stock") 
        client.request(r_inst)
        logger.info("Instrument Details fetched.")
    except Exception as e:
        logger.error(f"Inst Details failed: {e}")

    # 2. Exchanges
    logger.info("2. Exchanges...")
    try:
        r_ex = exchanges.ExchangeList()
        client.request(r_ex)
        logger.info(f"Exchanges count: {len(r_ex.response.get('Data', []))}")
    except Exception as e:
        logger.error(f"Exchanges failed: {e}")

    # 3. Languages
    logger.info("3. Languages...")
    try:
        r_lang = languages.Languages()
        client.request(r_lang)
        logger.info("Languages fetched.")
    except Exception as e:
        logger.error(f"Languages failed: {e}")

    # 4. TimeZones
    logger.info("4. TimeZones...")
    try:
        r_tz = timezones.TimeZones()
        client.request(r_tz)
        logger.info("TimeZones fetched.")
    except Exception as e:
        logger.error(f"TimeZones failed: {e}")

    print(json.dumps({"status": "success"}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
