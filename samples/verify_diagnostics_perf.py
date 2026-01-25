#!/usr/bin/env python3

"""
Cache & Performance Verification Sample

Measure API response times for repeated calls to check caching/network.

Usage:
    uv run libs/saxo_openapi/samples/verify_diagnostics_perf.py
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
    from saxo_openapi.endpoints.referencedata import currencies
except ImportError:
    sys.exit(1)


def main():
    load_dotenv()
    token = os.getenv("SAXO_24H_TOKEN")
    client = API(access_token=token)

    logger.info("Measuring Currencies endpoint performance (5 iterations)...")

    timings = []

    for i in range(5):
        start = time.time()
        try:
            r = currencies.Currencies()
            client.request(r)
            elapsed = (time.time() - start) * 1000  # ms
            timings.append(elapsed)
            logger.info(f"Iter {i + 1}: {elapsed:.2f} ms")
        except Exception as e:
            logger.error(f"Iter {i + 1} failed: {e}")

    if timings:
        avg = sum(timings) / len(timings)
        logger.info(f"Average response time: {avg:.2f} ms")

    print(json.dumps({"status": "success", "avg_ms": avg}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
