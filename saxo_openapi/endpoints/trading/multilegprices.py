"""Handle trading multileg prices endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/prices/multileg", "POST", 200)
class MultilegPrice(Trading):
    """Get multileg prices.

    See: docs/api/trading/prices.md#multilegprice
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(MultilegPrice, self).__init__()
        self.data = data


@endpoint("openapi/trade/v1/prices/multileg/subscriptions", "POST", 201)
class MultilegPriceSubscription(Trading):
    """Create a multileg price subscription.

    See: docs/api/trading/prices.md#multilegpricesubscription
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(MultilegPriceSubscription, self).__init__()
        self.data = data
