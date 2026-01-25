"""Handle root-services sessions endpoints.

See: docs/api/rootservices/sessions.md
"""

from typing import Any

from ..decorators import endpoint
from .base import RootService


@endpoint("openapi/root/v1/sessions/capabilities/")
class GetSessionCapabilities(RootService):
    """Get the sessions capabilities."""

    def __init__(self) -> None:
        super(GetSessionCapabilities, self).__init__()


@endpoint("openapi/root/v1/sessions/capabilities/", "PATCH", 202)
class ChangeSessionCapabilities(RootService):
    """Change sessions capabilities."""

    RESPONSE_DATA = None

    def __init__(self, data: dict[str, Any]) -> None:
        super(ChangeSessionCapabilities, self).__init__()
        self.data = data


@endpoint("openapi/root/v1/sessions/events/subscriptions/", "POST", 201)
class CreateSessionCapabilitiesSubscription(RootService):
    """Set up a new session capabilities subscription. The data stream will
    deliver updates from this point."""

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateSessionCapabilitiesSubscription, self).__init__()
        self.data = data


@endpoint(
    "openapi/root/v1/sessions/events/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class RemoveSessionCapabilitiesSubscription(RootService):
    """Removes the subscription identified by the specified reference id.
    (and streaming context id)."""

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveSessionCapabilitiesSubscription, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
