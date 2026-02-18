"""Handle accounthistory-performance v4 endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import AccountHistory


@endpoint("openapi/hist/v4/performance/{ClientKey}")
class AccountPerformanceV4(AccountHistory):
    """Get a collection of performance metrics for a specific account (v4).
    The account performance returns confidential information that is only
    allowed to be viewed by the account owner / owners. The required fields
    are ClientKey and either StandardPeriod or FromDate/ToDate.

    See: docs/api/accounthistory/performance.md
    """

    def __init__(self, ClientKey: str, params: dict[str, Any] | None = None) -> None:
        super().__init__(ClientKey=ClientKey)
        self.params = params
