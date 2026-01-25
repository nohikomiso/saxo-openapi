"""Handle valueadd-pricealerts endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ValueAdd


@endpoint("openapi/vas/v1/pricealerts/definitions/")
class GetAllAlerts(ValueAdd):
    """Get an unsorted list of all the price alert definitions belonging to
    the current user where the state matches the specified value.

    See: `docs/api/valueadd/pricealerts.md#getallalerts`
    """

    def __init__(self, params: dict[str, Any]) -> None:
        """Instantiate a GetAllAlerts request."""
        super(GetAllAlerts, self).__init__()
        self.params = params


@endpoint("openapi/vas/v1/pricealerts/definitions/{AlertDefinitionId}")
class GetAlertDefinition(ValueAdd):
    """Gets the specified price alert for the current user.

    See: `docs/api/valueadd/pricealerts.md#getalertdefinition`
    """

    def __init__(self, AlertDefinitionId: str) -> None:
        """Instantiate a GetAlertDefinition request."""
        super(GetAlertDefinition, self).__init__(AlertDefinitionId=AlertDefinitionId)


@endpoint("openapi/vas/v1/pricealerts/definitions/", "POST", 201)
class CreatePriceAlert(ValueAdd):
    """Create a new price alert definition.

    See: `docs/api/valueadd/pricealerts.md#createpricealert`
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Instantiate a CreatePriceAlert request."""
        super(CreatePriceAlert, self).__init__()
        self.data = data


@endpoint("openapi/vas/v1/pricealerts/definitions/{AlertDefinitionId}", "PUT", 204)
class UpdatePriceAlert(ValueAdd):
    """Update a price alert definition for the current user.

    See: `docs/api/valueadd/pricealerts.md#updatepricealert`
    """

    RESPONSE_DATA = None

    def __init__(self, AlertDefinitionId: str, data: dict[str, Any]) -> None:
        """Instantiate an UpdatePriceAlert request."""
        super(UpdatePriceAlert, self).__init__(AlertDefinitionId=AlertDefinitionId)
        self.data = data


@endpoint("openapi/vas/v1/pricealerts/definitions/{AlertDefinitionIds}", "DELETE", 204)
class DeletePriceAlert(ValueAdd):
    """Delete the specified price alert definitions.

    See: `docs/api/valueadd/pricealerts.md#deletepricealert`
    """

    RESPONSE_DATA = None

    def __init__(self, AlertDefinitionIds: str) -> None:
        """Instantiate a DeletePriceAlert request."""
        super(DeletePriceAlert, self).__init__(AlertDefinitionIds=AlertDefinitionIds)


@endpoint("openapi/vas/v1/pricealerts/usersettings/")
class GetUserNotificationSettings(ValueAdd):
    """Get the current user's price alert notification settings.

    See: `docs/api/valueadd/pricealerts.md#getusernotificationsettings`
    """

    def __init__(self) -> None:
        """Instantiate a GetUserNotificationSettings request."""
        super(GetUserNotificationSettings, self).__init__()


@endpoint("openapi/vas/v1/pricealerts/usersettings/", "PUT", 204)
class ModifyUserNotificationSettings(ValueAdd):
    """Modify the current user's price alert notification settings.

    See: `docs/api/valueadd/pricealerts.md#modifyusernotificationsettings`
    """

    RESPONSE_DATA = None

    def __init__(self, data: dict[str, Any]) -> None:
        """Instantiate a ModifyUserNotificationSettings request."""
        super(ModifyUserNotificationSettings, self).__init__()
        self.data = data
