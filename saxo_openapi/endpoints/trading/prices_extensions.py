# -*- encoding: utf-8 -*-

"""Handle trading prices extensions endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint(
    "openapi/trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}/MarginImpact",
    "PUT",
    200,
)
class MarginImpactSubscription(Trading):
    """Update margin impact subscription.

    See: docs/api/trading/prices.md#marginimpactsubscription
    """

    def __init__(self, ContextId: str, ReferenceId: str, data: dict[str, Any]) -> None:
        super(MarginImpactSubscription, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )
        self.data = data
