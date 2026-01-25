"""Handle root-services user endpoints."""

from ..decorators import endpoint
from .base import RootService


@endpoint("openapi/root/v1/user/")
class User(RootService):
    """Get information of current user.

    See: `docs/api/rootservices/user.md`
    """

    def __init__(self) -> None:
        """Instantiate a User request."""
        super(User, self).__init__()
