# -*- encoding: utf-8 -*-

"""Handle portfolio-exposure endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/exposure/instruments/me")
class NetInstrumentsExposureMe(Portfolio):
    """Returns a list instruments and net exposures.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self) -> None:
        super(NetInstrumentsExposureMe, self).__init__()


@endpoint("openapi/port/v1/exposure/instruments/")
class NetInstrumentExposureSpecific(Portfolio):
    """Returns a list instruments and net exposures.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(NetInstrumentExposureSpecific, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/exposure/instruments/subscriptions", "POST", 201)
class CreateExposureSubscription(Portfolio):
    """Sets up a subscription and returns an initial snapshot of list of
    instrument exposure specified by the parameters in the request.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateExposureSubscription, self).__init__()
        self.data = data


@endpoint(
    "openapi/port/v1/exposure/instruments/" "subscriptions/{ContextId}/", "DELETE", 202
)
class RemoveExposureSubscriptionsByTag(Portfolio):
    """Removes multiple all subscriptions for the current session on
    this resource, and frees all resources on the server.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        super(RemoveExposureSubscriptionsByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/port/v1/exposure/instruments/" "subscriptions/{ContextId}/{ReferenceId}",
    "DELETE",
    202,
)
class RemoveExposureSubscription(Portfolio):
    """Removes subscription for the current session identified by
    subscription id.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(RemoveExposureSubscription, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )


@endpoint("openapi/port/v1/exposure/currency/me")
class CurrencyExposureMe(Portfolio):
    """Returns a list of currencies and net exposures.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self) -> None:
        super(CurrencyExposureMe, self).__init__()


@endpoint("openapi/port/v1/exposure/currency/")
class CurrencyExposureSpecific(Portfolio):
    """Returns a list of currencies in which there is an exposure.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(CurrencyExposureSpecific, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/exposure/fxspot/me")
class FxSpotExposureMe(Portfolio):
    """Returns a list of currencies and net exposures.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self) -> None:
        super(FxSpotExposureMe, self).__init__()


@endpoint("openapi/port/v1/exposure/fxspot/")
class FxSpotExposureSpecific(Portfolio):
    """Returns a list of currencies in which there is an exposure.

    See: libs/saxo_openapi/docs/api/portfolio/exposure.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(FxSpotExposureSpecific, self).__init__()
        self.params = params
