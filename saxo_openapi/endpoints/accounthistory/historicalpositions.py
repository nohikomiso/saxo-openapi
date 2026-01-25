# -*- encoding: utf-8 -*-

"""Handle account endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import AccountHistory


@endpoint("openapi/hist/v3/positions/{ClientKey}")
class HistoricalPositions(AccountHistory):
    """Get a list of historical positions for a specific account owned
    by a client. The required fields are ClientKey and either StandardPeriod
    or FromDate/ToDate.

    See: docs/api/accounthistory/historicalpositions.md
    """

    def __init__(self, ClientKey: str, params: dict[str, Any]) -> None:
        super(HistoricalPositions, self).__init__(ClientKey=ClientKey)
        self.params = params
