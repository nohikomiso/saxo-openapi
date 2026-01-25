# -*- encoding: utf-8 -*-

"""Handle trading-orders endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v2/orders", "POST")
class Order(Trading):
    """Place a new order.

    See: docs/api/trading/orders.md#order
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(Order, self).__init__()
        self.data = data


@endpoint("openapi/trade/v2/orders", "PATCH")
class ChangeOrder(Trading):
    """Change one or more existing orders.

    See: docs/api/trading/orders.md#changeorder
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(ChangeOrder, self).__init__()
        self.data = data


@endpoint("openapi/trade/v2/orders/{OrderIds}", "DELETE")
class CancelOrders(Trading):
    """Cancel one or more orders.

    See: docs/api/trading/orders.md#cancelorders
    """

    def __init__(self, OrderIds: str, params: dict[str, Any]) -> None:
        super(CancelOrders, self).__init__(OrderIds=OrderIds)
        self.params = params


@endpoint("openapi/trade/v2/orders/precheck", "POST")
class PrecheckOrder(Trading):
    """Precheck an order.

    See: docs/api/trading/orders.md#precheckorder
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(PrecheckOrder, self).__init__()
        self.data = data
