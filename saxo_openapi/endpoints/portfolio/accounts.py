# -*- encoding: utf-8 -*-

"""Handle portfolio-account endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/accounts/{AccountKey}")
class AccountDetails(Portfolio):
    """Get details about a single account.

    See: docs/api/portfolio/accounts.md
    """

    def __init__(self, AccountKey: str) -> None:
        super(AccountDetails, self).__init__(AccountKey=AccountKey)


@endpoint("openapi/port/v1/accounts/me")
class AccountsMe(Portfolio):
    """Get all accounts under a particular client to which the logged
    in user belongs.

    See: docs/api/portfolio/accounts.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(AccountsMe, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/accounts/")
class AccountListByClient(Portfolio):
    """Get all accounts owned by the specified client.

    See: docs/api/portfolio/accounts.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(AccountListByClient, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/accounts/{AccountKey}", "PATCH", 204)
class AccountUpdate(Portfolio):
    """Update account details. Particularly the user account shield value,
    the benchmark instrument or the account display name.

    See: docs/api/portfolio/accounts.md
    """

    RESPONSE_DATA = None

    def __init__(self, AccountKey: str, data: dict[str, Any]) -> None:
        super(AccountUpdate, self).__init__(AccountKey=AccountKey)
        self.data = data


@endpoint("openapi/port/v1/accounts/{AccountKey}/reset", "PUT", 204)
class AccountReset(Portfolio):
    """Reset the trial account. Cannot be used in live environment.

    See: docs/api/portfolio/accounts.md
    """

    RESPONSE_DATA = None

    def __init__(self, AccountKey: str, data: dict[str, Any]) -> None:
        super(AccountReset, self).__init__(AccountKey=AccountKey)
        self.data = data


@endpoint("openapi/port/v1/accounts/subscriptions/", "POST", 201)
class SubscriptionCreate(Portfolio):
    """Set up a subscription and returns an initial snapshot containing
    a list of accounts as specified by the parameters in the request.

    See: docs/api/portfolio/accounts.md
    """

    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, data: dict[str, Any]) -> None:
        super(SubscriptionCreate, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/accounts/subscriptions/{ContextId}/", "DELETE", 202)
class SubscriptionRemoveByTag(Portfolio):
    """Remove all subscriptions for the current session on this resource
    marked with a specific tag, and frees all resources on the server.

    See: docs/api/portfolio/accounts.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(SubscriptionRemoveByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/port/v1/accounts/subscriptions/" "{ContextId}/{ReferenceId}/",
    "DELETE",
    202,
)
class SubscriptionRemoveById(Portfolio):
    """Remove subscription for the current session identified by
    subscription Id.

    See: docs/api/portfolio/accounts.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(SubscriptionRemoveById, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )
