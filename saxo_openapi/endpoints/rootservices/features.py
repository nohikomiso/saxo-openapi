"""Handle root-services features endpoints.

See: docs/api/rootservices/features.md
"""

from typing import Any

from ..decorators import endpoint
from .base import RootService


@endpoint("openapi/root/v1/features/availability/")
class Availability(RootService):
    """Get the availability of all features."""

    def __init__(self) -> None:
        super(Availability, self).__init__()


@endpoint("openapi/root/v1/features/availability/subscriptions", "POST", 201)
class CreateAvailabilitySubscription(RootService):
    """Create a feature availability subscription."""

    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateAvailabilitySubscription, self).__init__()
        self.data = data


@endpoint(
    "openapi/root/v1/features/availability/subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class RemoveAvailabilitySubscription(RootService):
    """Removes the subscription identified by the specified reference id
    (and streaming context id).
    """

    # this endpoint returns an empty string as data: ''
    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveAvailabilitySubscription, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
