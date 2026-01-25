# -*- encoding: utf-8 -*-

"""Handle referencedata-instruments endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/instruments/")
class Instruments(ReferenceData):
    """Get a list of summary information for all instruments and options.

    See: docs/api/referencedata/instruments.md#instruments
    """

    def __init__(self, params: dict[str, Any]) -> None:
        super(Instruments, self).__init__()
        self.params = params


@endpoint("openapi/ref/v1/instruments/details")
class InstrumentsDetails(ReferenceData):
    """Get detailed information on a list of instruments.

    See: docs/api/referencedata/instruments.md#instrumentsdetails
    """

    def __init__(self, params: dict[str, Any]) -> None:
        super(InstrumentsDetails, self).__init__()
        self.params = params


@endpoint("openapi/ref/v1/instruments/details/{Uic}/{AssetType}")
class InstrumentDetails(ReferenceData):
    """Get detailed information for a specific instrument.

    See: docs/api/referencedata/instruments.md#instrumentdetails
    """

    def __init__(
        self, Uic: int, AssetType: str, params: dict[str, Any] | None = None
    ) -> None:
        super(InstrumentDetails, self).__init__(Uic=Uic, AssetType=AssetType)
        self.params = params


@endpoint("openapi/ref/v1/instruments/contractoptionspaces/{OptionRootId}")
class ContractoptionSpaces(ReferenceData):
    """Get contractoption data.

    See: docs/api/referencedata/instruments.md#contractoptionspaces
    """

    def __init__(self, OptionRootId: str, params: dict[str, Any] | None = None) -> None:
        super(ContractoptionSpaces, self).__init__(OptionRootId=OptionRootId)
        self.params = params


@endpoint("openapi/ref/v1/instruments/futuresspaces/{ContinuousFuturesUic}")
class FuturesSpaces(ReferenceData):
    """Get futures spaces data.

    See: docs/api/referencedata/instruments.md#futuresspaces
    """

    def __init__(self, ContinuousFuturesUic: int) -> None:
        super(FuturesSpaces, self).__init__(ContinuousFuturesUic=ContinuousFuturesUic)


@endpoint("openapi/ref/v1/instruments/tradingschedule/{Uic}/{AssetType}")
class TradingSchedule(ReferenceData):
    """Get TradingSchedule data.

    See: docs/api/referencedata/instruments.md#tradingschedule
    """

    def __init__(self, Uic: int, AssetType: str) -> None:
        super(TradingSchedule, self).__init__(Uic=Uic, AssetType=AssetType)
