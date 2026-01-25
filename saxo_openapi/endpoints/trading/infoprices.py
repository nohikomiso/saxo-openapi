# -*- encoding: utf-8 -*-

"""Handle trading-infoprices endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/infoprices")
class InfoPrice(Trading):
    """Get an info price for an instrument.

    See: docs/api/trading/infoprices.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(InfoPrice, self).__init__()
        self.params = params


@endpoint("openapi/trade/v1/infoprices/list")
class InfoPrices(Trading):
    """Get a list of info prices for multiple instruments.

    See: docs/api/trading/infoprices.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(InfoPrices, self).__init__()
        self.params = params


@endpoint("openapi/trade/v1/infoprices/subscriptions", "POST", 201)
class CreateInfoPriceSubscription(Trading):
    """Create an info price subscription.

    See: docs/api/trading/infoprices.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateInfoPriceSubscription, self).__init__()
        self.data = data


@endpoint("openapi/trade/v1/infoprices/subscriptions/{ContextId}", "DELETE", 202)
class RemoveInfoPriceSubscriptionsByTag(Trading):
    """Remove one or more infoprice subscriptions by tag.

    See: docs/api/trading/infoprices.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(RemoveInfoPriceSubscriptionsByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/trade/v1/infoprices/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class RemoveInfoPriceSubscriptionById(Trading):
    """Remove an info price subscription by ID.

    See: docs/api/trading/infoprices.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveInfoPriceSubscriptionById, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )


@endpoint("openapi/trade/v1/infoprices/list/anonymous")
class AnonymousInfoPrices(Trading):
    """Get a list of info prices for multiple instruments without authentication.

    See: docs/api/trading/infoprices.md#anonymousinfoprices
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(AnonymousInfoPrices, self).__init__()
        self.params = params
