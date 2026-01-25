"""Handle referencedata-languages endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/languages/")
class Languages(ReferenceData):
    """Get a list containing all the languages supported by Saxo Bank

    See: docs/api/referencedata/languages.md
    """

    def __init__(self) -> None:
        """Instantiate a Languages request."""
        super(Languages, self).__init__()
