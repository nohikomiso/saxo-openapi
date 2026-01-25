"""Handle referencedata-algostrategies endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import ReferenceData


@endpoint("openapi/ref/v1/algostrategies/")
class AlgoStrategies(ReferenceData):
    """Retrieve a list of strategies with detailed information

    See: docs/api/referencedata/algostrategies.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        """Instantiate an AlgoStrategies request.

        Parameters
        ----------
        params: dict (required)
            dict representing the querystring parameters
        """
        super(AlgoStrategies, self).__init__()
        self.params = params


@endpoint("openapi/ref/v1/algostrategies/{Name}")
class AlgoStrategyDetails(ReferenceData):
    """Retrieve detailed information about a specific Strategy

    See: docs/api/referencedata/algostrategies.md
    """

    def __init__(self, Name: str) -> None:
        """Instantiate an AlgoStrategyDetails request.

        Parameters
        ----------
        Name: string (required)
            Name of the strategy
        """
        super(AlgoStrategyDetails, self).__init__(Name=Name)
