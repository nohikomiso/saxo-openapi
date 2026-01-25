"""
Contrib module - high-level helper classes for trading.

These classes are NOT imported at package level to avoid circular imports.
Import directly from submodules:

    from saxo_openapi.contrib.trader import SaxoTrader
    from saxo_openapi.contrib.option_trader import OptionTrader
    from saxo_openapi.contrib.option_finder import OptionFinder
    from saxo_openapi.contrib.session import account_info
"""

# 循環インポートを避けるため、トップレベルではインポートしない
# 必要な場合は各サブモジュールから直接インポートすること

__all__ = [
    "session",
    "trader",
    "orders",
    "option_finder",
    "option_trader",
    "option_types",
]
