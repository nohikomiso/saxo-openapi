# -*- encoding: utf-8 -*-

"""Handle portfolio-users endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/users/me")
class UsersMe(Portfolio):
    """Get details about the logged in user.

    See: libs/saxo_openapi/docs/api/portfolio/users.md
    """

    def __init__(self) -> None:
        super(UsersMe, self).__init__()


@endpoint("openapi/port/v1/users")
class Users(Portfolio):
    """Get all users under a particular owner.

    See: libs/saxo_openapi/docs/api/portfolio/users.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(Users, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/users/{UserKey}")
class UserDetails(Portfolio):
    """Get the details about a user.

    See: libs/saxo_openapi/docs/api/portfolio/users.md
    """

    def __init__(self, UserKey: str) -> None:
        super(UserDetails, self).__init__(UserKey=UserKey)


@endpoint("openapi/port/v1/users/me", "PATCH", 204)
class UserUpdate(Portfolio):
    """Enables the user to update preferred language, culture and timezone.

    See: libs/saxo_openapi/docs/api/portfolio/users.md
    """

    RESPONSE_DATA = None

    def __init__(self, data: dict[str, Any]) -> None:
        super(UserUpdate, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/users/me/entitlements")
class UsersMeEntitlements(Portfolio):
    """Get the entitlements for the logged-in user.

    See: docs/api/portfolio/users.md#usersmeentitlements
    """

    def __init__(self) -> None:
        super(UsersMeEntitlements, self).__init__()


@endpoint("openapi/port/v1/users/{UserKey}/entitlements")
class UsersEntitlements(Portfolio):
    """Get the entitlements for a specific user.

    See: docs/api/portfolio/users.md#usersentitlements
    """

    def __init__(self, UserKey: str) -> None:
        super(UsersEntitlements, self).__init__(UserKey=UserKey)
