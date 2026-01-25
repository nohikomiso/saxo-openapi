"""Handle referencedata-timezones endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/timezones/")
class TimeZones(ReferenceData):
    """Get a list all the time zones supported by Saxo Bank

    See: docs/api/referencedata/timezones.md
    """

    def __init__(self) -> None:
        """Instantiate a TimeZones request."""
        super(TimeZones, self).__init__()
