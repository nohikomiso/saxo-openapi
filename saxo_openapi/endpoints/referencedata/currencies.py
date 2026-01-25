"""Handle referencedata-currencies endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/currencies/")
class Currencies(ReferenceData):
    """Get a list all supported currencies

    See: docs/api/referencedata/currencies.md
    """

    def __init__(self) -> None:
        """Instantiate a Currencies request."""
        super(Currencies, self).__init__()
