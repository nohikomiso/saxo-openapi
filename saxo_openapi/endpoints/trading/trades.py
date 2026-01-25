# -*- encoding: utf-8 -*-

"""Handle trading trades endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v2/trades", "POST", 201)
class Trade(Trading):
    """Execute a trade.

    See: docs/api/trading/trades.md#trade
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(Trade, self).__init__()
        self.data = data
