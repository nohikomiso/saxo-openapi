"""Handle accounthistory-accountvalues endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import AccountHistory


@endpoint("openapi/hist/v3/accountvalues/{ClientKey}/")
class AccountSummary(AccountHistory):
    """Get 'rolled up performance' for the accounts of specified client.

    See: docs/api/accounthistory/accountvalues.md
    """

    def __init__(self, ClientKey: str, params: dict[str, Any] | None = None) -> None:
        super().__init__(ClientKey=ClientKey)
        self.params = params
