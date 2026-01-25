"""Handle portfolio-netpositions endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/netpositions/{NetPositionId}")
class SingleNetPosition(Portfolio):
    """Get a single net position.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    def __init__(self, NetPositionId: str, params: dict[str, Any] | None = None) -> None:
        super(SingleNetPosition, self).__init__(NetPositionId=NetPositionId)
        self.params = params


@endpoint("openapi/port/v1/netpositions/{NetPositionId}/details")
class SingleNetPositionDetails(Portfolio):
    """Get a single net position details.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    def __init__(self, NetPositionId: str, params: dict[str, Any] | None = None) -> None:
        super(SingleNetPositionDetails, self).__init__(NetPositionId=NetPositionId)
        self.params = params


@endpoint("openapi/port/v1/netpositions/me")
class NetPositionsMe(Portfolio):
    """Get netpositions for the logged-in client.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(NetPositionsMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/netpositions")
class NetPositionsQuery(Portfolio):
    """Get netpositions for a client, account group, account or position.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(NetPositionsQuery, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/netpositions/subscriptions", "POST", 201)
class NetPositionListSubscription(Portfolio):
    """Create a subscription on a list of net positions and make it active.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(NetPositionListSubscription, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/netpositions/subscriptions/{ContextId}/", "DELETE", 202)
class NetPositionSubscriptionRemoveMultiple(Portfolio):
    """Remove multiple all subscriptions for the current session on this
    resource, and frees all resources on the server.

    See: libs/saxo_openapi/docs/api/portfolio/netpositions.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(NetPositionSubscriptionRemoveMultiple, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/port/v1/netpositions/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class NetPositionSubscriptionRemoveById(Portfolio):
    """Removes subscription for the current session identified by
    subscription id.

    See: docs/api/portfolio/netpositions.md#netpositionsubscriptionremovebyid
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(NetPositionSubscriptionRemoveById, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
