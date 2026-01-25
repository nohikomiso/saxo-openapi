"""Handle portfolio-accountgroups endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/accountgroups/{AccountGroupKey}")
class AccountGroupDetails(Portfolio):
    """Get details about a single account group.

    See: docs/api/portfolio/accountgroups.md
    """

    def __init__(self, AccountGroupKey: str, params: dict[str, Any] | None = None) -> None:
        super(AccountGroupDetails, self).__init__(AccountGroupKey=AccountGroupKey)
        self.params = params


@endpoint("openapi/port/v1/accountgroups/me")
class AccountGroupsMe(Portfolio):
    """Get all accounts groups under a particular client to which the logged
    in user belongs.

    See: docs/api/portfolio/accountgroups.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(AccountGroupsMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/accountgroups/")
class AccountGroupsList(Portfolio):
    """Get a list of all account groups used by the specified client.

    See: docs/api/portfolio/accountgroups.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(AccountGroupsList, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/accountgroups/{AccountGroupKey}", "PATCH", 204)
class AccountGroupUpdate(Portfolio):
    """Update account group settings. Particularly the account group
    AccountValueProtectionLimit.

    See: docs/api/portfolio/accountgroups.md
    """

    RESPONSE_DATA = None

    def __init__(self, AccountGroupKey: str, params: dict[str, Any] | None, data: dict[str, Any]) -> None:
        super(AccountGroupUpdate, self).__init__(AccountGroupKey=AccountGroupKey)
        self.params = params
        self.data = data
