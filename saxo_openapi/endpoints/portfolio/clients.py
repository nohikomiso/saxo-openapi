# -*- encoding: utf-8 -*-

"""Handle portfolio-clients endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/clients/me")
class ClientDetailsMe(Portfolio):
    """Get details about logged-in user's client.

    See: docs/api/portfolio/clients.md
    """

    def __init__(self) -> None:
        super(ClientDetailsMe, self).__init__()


@endpoint("openapi/port/v1/clients/{ClientKey}")
class ClientDetails(Portfolio):
    """Get details about a client.

    See: docs/api/portfolio/clients.md
    """

    def __init__(self, ClientKey: str) -> None:
        super(ClientDetails, self).__init__(ClientKey=ClientKey)


@endpoint("openapi/port/v1/clients/me", "PATCH", 204)
class ClientDetailsUpdate(Portfolio):
    """Enables user of the client to switch position netting
    mode of its own.

    See: docs/api/portfolio/clients.md
    """

    RESPONSE_DATA = None

    def __init__(self, data: dict[str, Any]) -> None:
        super(ClientDetailsUpdate, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/clients/")
class ClientDetailsByOwner(Portfolio):
    """Get details about clients under a particular owner.

    See: docs/api/portfolio/clients.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(ClientDetailsByOwner, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/clients/", "PATCH", 204)
class ClientSwitchPosNettingMode(Portfolio):
    """Enables IB to switch position netting mode and change account
    value protection limit on behalf of its clients.

    See: docs/api/portfolio/clients.md
    """

    RESPONSE_DATA = None

    def __init__(self, params: dict[str, Any] | None, data: dict[str, Any]) -> None:
        super(ClientSwitchPosNettingMode, self).__init__()
        self.params = params
        self.data = data
