# -*- encoding: utf-8 -*-

"""Handle trading-prices endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/prices/subscriptions", "POST", 201)
class CreatePriceSubscription(Trading):
    """Sets up an active price subscription on an instrument.

    See: docs/api/trading/prices.md#createpricesubscription
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreatePriceSubscription, self).__init__()
        self.data = data


@endpoint("openapi/trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}", "PUT", 204)
class MarginImpactRequest(Trading):
    """Request margin impact to come on one of the next following price updates.

    See: docs/api/trading/prices.md#marginimpactrequest
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(MarginImpactRequest, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )


@endpoint("openapi/trade/v1/prices/subscriptions/{ContextId}/", "DELETE", 202)
class PriceSubscriptionRemoveByTag(Trading):
    """Remove multiple subscriptions for the given ContextId.

    See: docs/api/trading/prices.md#pricesubscriptionremovebytag
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(PriceSubscriptionRemoveByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 202
)
class PriceSubscriptionRemove(Trading):
    """Removes subscription for the current session identified by subscription id.

    See: docs/api/trading/prices.md#pricesubscriptionremove
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(PriceSubscriptionRemove, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )
