"""Handle portfolio-closedposition endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/closedpositions/")
class ClosedPositionList(Portfolio):
    """Returns a list of closed positions fulfilling the criteria
    specified by the query string parameters.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionList, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/closedpositions/{ClosedPositionId}")
class ClosedPositionById(Portfolio):
    """Get a single position by the ClosedPositionId.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    def __init__(self, ClosedPositionId: str, params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionById, self).__init__(ClosedPositionId=ClosedPositionId)
        self.params = params


@endpoint("openapi/port/v1/closedpositions/{ClosedPositionId}/details/")
class ClosedPositionDetails(Portfolio):
    """Gets detailed information about a single position as specified by
    the query parameters

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    def __init__(self, ClosedPositionId: str, params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionDetails, self).__init__(ClosedPositionId=ClosedPositionId)
        self.params = params


@endpoint("openapi/port/v1/closedpositions/me")
class ClosedPositionsMe(Portfolio):
    """Returns a list of closed positions fulfilling the criteria specified
    by the query string parameters.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionsMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/closedpositions/subscriptions/", "POST", 201)
class ClosedPositionSubscription(Portfolio):
    """Sets up a subscription and returns an initial snapshot of list of
    closed positions specified by the parameters in the request.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    def __init__(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionSubscription, self).__init__()
        self.data = data
        self.params = params


@endpoint(
    "openapi/port/v1/closedpositions/subscriptions/{ContextId}/{ReferenceId}",
    "PATCH",
    200,
)
class ClosedPositionSubscriptionUpdate(Portfolio):
    """Extends or reduces the page size, number of positions shown, on
    a running closed positions subscription.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str, data: dict[str, Any]) -> None:
        super(ClosedPositionSubscriptionUpdate, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
        self.data = data


@endpoint("openapi/port/v1/closedpositions/subscriptions/{ContextId}", "DELETE", 202)
class ClosedPositionSubscriptionsRemove(Portfolio):
    """Removes multiple all subscriptions for the current session on this
    resource, and frees all resources on the server.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(ClosedPositionSubscriptionsRemove, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/port/v1/closedpositions/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class ClosedPositionSubscriptionRemoveById(Portfolio):
    """Removes subscription for the current session identified by
    subscription id.

    See: libs/saxo_openapi/docs/api/portfolio/closedpositions.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(ClosedPositionSubscriptionRemoveById, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
