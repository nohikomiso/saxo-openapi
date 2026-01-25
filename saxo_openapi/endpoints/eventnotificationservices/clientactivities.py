# -*- encoding: utf-8 -*-

"""Handle ens - client activities endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ENS


@endpoint("openapi/ens/v1/activities/subscriptions", "POST", 201)
class CreateSubscriptionForClientEvents(ENS):
    """Set up an active subscription to listen client events.

    See: `docs/api/eventnotificationservices/clientactivities.md#createsubscriptionforclientevents`
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Instantiate a CreateSubscriptionForClientEvents request."""
        super(CreateSubscriptionForClientEvents, self).__init__()
        self.data = data


@endpoint(
    "openapi/ens/v1/activities/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 202
)
class RemoveSubscription(ENS):
    """Remove subscription for the current session identified by subscription
    id.

    See: `docs/api/eventnotificationservices/clientactivities.md#removesubscription`
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        """Instantiate a RemoveSubscription request."""
        super(RemoveSubscription, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )


@endpoint("openapi/ens/v1/activities/subscriptions/{ContextId}", "DELETE", 202)
class RemoveSubscriptions(ENS):
    """Remove multiple/all subscriptions for the current session on this
    resource and free all resources on the server.

    See: `docs/api/eventnotificationservices/clientactivities.md#removesubscriptions`
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        """Instantiate a RemoveSubscriptions request."""
        super(RemoveSubscriptions, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint("openapi/ens/v1/activities")
class GetActivities(ENS):
    """Return a list of activities specified by the parameters in the
    request.

    See: `docs/api/eventnotificationservices/clientactivities.md#getactivities`
    """

    def __init__(self, params: dict[str, Any]) -> None:
        """Instantiate a GetActivities request."""
        super(GetActivities, self).__init__()
        self.params = params
