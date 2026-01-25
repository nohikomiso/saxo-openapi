# -*- encoding: utf-8 -*-

"""Handle trading-messages endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/messages")
class GetTradeMessages(Trading):
    """Get trade messages for the current user.

    See: docs/api/trading/messages.md
    """

    def __init__(self) -> None:
        super(GetTradeMessages, self).__init__()


@endpoint("openapi/trade/v1/messages/seen/{MessageId}", "PUT", 204)
class MarkMessageAsSeen(Trading):
    """Mark a message as seen.

    See: docs/api/trading/messages.md
    """

    RESPONSE_DATA = None

    def __init__(self, MessageId: str) -> None:
        super(MarkMessageAsSeen, self).__init__(MessageId=MessageId)


@endpoint("openapi/trade/v1/messages/subscriptions", "POST", 201)
class CreateTradeMessageSubscription(Trading):
    """Create a subscription on trade messages.

    See: docs/api/trading/messages.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateTradeMessageSubscription, self).__init__()
        self.data = data


@endpoint(
    "openapi/trade/v1/messages/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class RemoveTradeMessageSubscriptionById(Trading):
    """Remove a trade message subscription by ID.

    See: docs/api/trading/messages.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveTradeMessageSubscriptionById, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )


@endpoint("openapi/trade/v1/messages/subscriptions/{ContextId}", "DELETE", 202)
class RemoveTradeMessageSubscriptions(Trading):
    """Remove trade message subscriptions.

    See: docs/api/trading/messages.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(RemoveTradeMessageSubscriptions, self).__init__(ContextId=ContextId)
        self.params = params
