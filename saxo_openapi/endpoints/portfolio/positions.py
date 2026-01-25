"""Handle portfolio-positions endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/positions/{PositionId}")
class SinglePosition(Portfolio):
    """Get a single position.

    See: docs/api/portfolio/positions.md#singleposition
    """

    def __init__(self, PositionId: str, params: dict[str, Any]) -> None:
        super(SinglePosition, self).__init__(PositionId=PositionId)
        self.params = params


@endpoint("openapi/port/v1/positions/{PositionId}/details")
class SinglePositionDetails(Portfolio):
    """Get a single position details.

    See: docs/api/portfolio/positions.md#singlepositiondetails
    """

    def __init__(self, PositionId: str, params: dict[str, Any]) -> None:
        super(SinglePositionDetails, self).__init__(PositionId=PositionId)
        self.params = params


@endpoint("openapi/port/v1/positions/me")
class PositionsMe(Portfolio):
    """Get positions for the logged-in client.

    See: docs/api/portfolio/positions.md#positionsme
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(PositionsMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/positions")
class PositionsQuery(Portfolio):
    """Get positions for a client, account group, account or position.

    See: docs/api/portfolio/positions.md#positionsquery
    """

    def __init__(self, params: dict[str, Any]) -> None:
        super(PositionsQuery, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/positions/subscriptions", "POST", 201)
class PositionListSubscription(Portfolio):
    """Sets up a subscription and returns an initial snapshot of list of positions.

    See: docs/api/portfolio/positions.md#positionlistsubscription
    """

    def __init__(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> None:
        super(PositionListSubscription, self).__init__()
        self.params = params
        self.data = data


@endpoint("openapi/port/v1/positions/subscriptions/{ContextId}/{ReferenceId}", "PATCH", 202)
class PositionSubscriptionPageSize(Portfolio):
    """Extends or reduces the page size on a running positions subscription.

    See: docs/api/portfolio/positions.md#positionsubscriptionpagesize
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str, data: dict[str, Any]) -> None:
        super(PositionSubscriptionPageSize, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
        self.data = data


@endpoint("openapi/port/v1/positions/subscriptions/{ContextId}/", "DELETE", 202)
class PositionSubscriptionRemoveMultiple(Portfolio):
    """Remove multiple subscriptions for the given ContextId.

    See: docs/api/portfolio/positions.md#positionsubscriptionremovemultiple
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(PositionSubscriptionRemoveMultiple, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint("openapi/port/v1/positions/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 202)
class PositionSubscriptionRemove(Portfolio):
    """Removes subscription for the current session identified by subscription id.

    See: docs/api/portfolio/positions.md#positionsubscriptionremove
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(PositionSubscriptionRemove, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
