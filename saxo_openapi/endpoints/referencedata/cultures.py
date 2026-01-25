# -*- encoding: utf-8 -*-

"""Handle referencedata-cultures endpoints."""

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/cultures/")
class Cultures(ReferenceData):
    """Get a list all the cultures for user preference localization supported by Saxo Bank

    See: docs/api/referencedata/cultures.md
    """

    def __init__(self) -> None:
        """Instantiate a Cultures request."""
        super(Cultures, self).__init__()
