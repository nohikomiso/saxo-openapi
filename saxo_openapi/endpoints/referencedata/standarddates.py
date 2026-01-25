# -*- encoding: utf-8 -*-

"""Handle referencedata-standarddates endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/standarddates/forwardtenor/{Uic}")
class ForwardTenorDates(ReferenceData):
    """Get a list of forward tenor dates for an UIC

    See: docs/api/referencedata/standarddates.md
    """

    def __init__(self, Uic: int, params: dict[str, Any]) -> None:
        """Instantiate a ForwardTenorDates request.

        Parameters
        ----------
        Uic: int (required)
            the Uic code of the instrument
        params: dict (required)
            dict with parameters representing the querystring
        """
        super(ForwardTenorDates, self).__init__(Uic=Uic)
        self.params = params


@endpoint("openapi/ref/v1/standarddates/fxoptionexpiry/{Uic}")
class FXOptionExpiryDates(ReferenceData):
    """Get a list of FX option expiry dates for an UIC

    See: docs/api/referencedata/standarddates.md
    """

    def __init__(self, Uic: int) -> None:
        """Instantiate a FXOptionExpiryDates request.

        Parameters
        ----------
        Uic: int (required)
            the Uic code of the instrument
        """
        super(FXOptionExpiryDates, self).__init__(Uic=Uic)
