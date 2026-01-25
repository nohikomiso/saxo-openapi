"""Handle referencedata-countries endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/countries/")
class Countries(ReferenceData):
    """Retrieve a list all the countries supported by Saxo Bank

    See: docs/api/referencedata/countries.md
    """

    def __init__(self) -> None:
        """Instantiate a Countries request."""
        super(Countries, self).__init__()
