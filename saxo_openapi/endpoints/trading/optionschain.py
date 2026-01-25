"""Handle trading-optionschain endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/optionschain/subscriptions", "POST", 201)
class OptionsChainSubscriptionCreate(Trading):
    """Create an options chain subscription.

    See: docs/api/trading/optionschain.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(OptionsChainSubscriptionCreate, self).__init__()
        self.data = data


@endpoint(
    "openapi/trade/v1/optionschain/subscriptions/{ContextId}/{ReferenceId}",
    "PATCH",
    204,
)
class OptionsChainSubscriptionModify(Trading):
    """Modify an options chain subscription.

    See: docs/api/trading/optionschain.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str, data: dict[str, Any]) -> None:
        super(OptionsChainSubscriptionModify, self).__init__(ReferenceId=ReferenceId, ContextId=ContextId)
        self.data = data


@endpoint(
    "openapi/trade/v1/optionschain/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class OptionsChainSubscriptionRemove(Trading):
    """Remove an options chain subscription.

    See: docs/api/trading/optionschain.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(OptionsChainSubscriptionRemove, self).__init__(ReferenceId=ReferenceId, ContextId=ContextId)


@endpoint(
    "openapi/trade/v1/optionschain/subscriptions/{ContextId}/{ReferenceId}/ResetATM",
    "PUT",
    204,
)
class OptionsChainSubscriptionResetATM(Trading):
    """Reset an options chain subscription to ATM.

    See: docs/api/trading/optionschain.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(OptionsChainSubscriptionResetATM, self).__init__(ReferenceId=ReferenceId, ContextId=ContextId)
