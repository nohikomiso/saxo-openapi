"""Handle portfolio-orders endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/orders/{ClientKey}/{OrderId}")
class GetOpenOrder(Portfolio):
    """get a specific open order of a client.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    def __init__(self, ClientKey: str, OrderId: str, params: dict[str, Any] | None = None) -> None:
        super(GetOpenOrder, self).__init__(ClientKey=ClientKey, OrderId=OrderId)
        self.params = params


@endpoint("openapi/port/v1/orders/me/")
class GetOpenOrdersMe(Portfolio):
    """get all the open orders on a client to which the logged in
    user belongs.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(GetOpenOrdersMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/orders/{OrderId}/details/")
class OrderDetails(Portfolio):
    """Get detailed information about a single open order as specified
    by the query parameters.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    def __init__(self, OrderId: str, params: dict[str, Any] | None = None) -> None:
        super(OrderDetails, self).__init__(OrderId=OrderId)
        self.params = params


@endpoint("openapi/port/v1/orders/")
class GetAllOpenOrders(Portfolio):
    """all the open orders on an account or a client.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(GetAllOpenOrders, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/orders/subscriptions", "POST", 201)
class CreateOpenOrdersSubscription(Portfolio):
    """Set up a subscription and returns an initial snapshot of list
    of orders specified by the parameters in the request.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateOpenOrdersSubscription, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/orders/subscriptions/{ContextId}/", "DELETE", 202)
class RemoveOpenOrderSubscriptionsByTag(Portfolio):
    """Remove multiple subscriptions for the current session on this
    resource. Optionally with with specified Tag.

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(RemoveOpenOrderSubscriptionsByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint("openapi/port/v1/orders/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 202)
class RemoveOpenOrderSubscription(Portfolio):
    """Remove a subscription for the current session identified by
    subscription id

    See: libs/saxo_openapi/docs/api/portfolio/orders.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveOpenOrderSubscription, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
