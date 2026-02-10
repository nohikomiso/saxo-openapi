"""Handle root-services subscriptions endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import RootService


@endpoint("openapi/root/v1/subscriptions/{ContextId}", "DELETE", 202)
class RemoveMultipleActiveSubscriptions(RootService):
    """Removes multiple subscriptions for the current session, and frees all
    resources on the server.

    See: `docs/api/rootservices/subscriptions.md`
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any]) -> None:
        """Instantiate a RemoveMultipleActiveSubscriptions request."""
        super().__init__(ContextId=ContextId)
        self.params = params
