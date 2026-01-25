"""Handle referencedata-currencypairs endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/currencypairs/")
class CurrencyPairs(ReferenceData):
    """Get data on currency pairs

    See: docs/api/referencedata/currencypairs.md
    """

    def __init__(self) -> None:
        """Instantiate a Currency Pairs request."""
        super(CurrencyPairs, self).__init__()
