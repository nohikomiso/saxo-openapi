# -*- encoding: utf-8 -*-

"""Handle referencedata-exchanges endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/exchanges/")
class ExchangeList(ReferenceData):
    """Retrieve a list of exchanges with detailed information

    See: docs/api/referencedata/exchanges.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        """Instantiate an ExchangeList request.

        Parameters
        ----------
        params: dict (optional)
            dict representing querystring parameters
        """
        super(ExchangeList, self).__init__()
        self.params = params


@endpoint("openapi/ref/v1/exchanges/{ExchangeId}")
class ExchangeDetails(ReferenceData):
    """Retrieves detailed information about a specific exchange

    See: docs/api/referencedata/exchanges.md
    """

    def __init__(self, ExchangeId: str) -> None:
        """Instantiate an ExchangeDetails request.

        Parameters
        ----------
        ExchangeId: string (required)
            the ExchangeId
        """
        super(ExchangeDetails, self).__init__(ExchangeId=ExchangeId)
