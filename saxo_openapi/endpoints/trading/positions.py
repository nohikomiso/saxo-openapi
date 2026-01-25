"""Handle trading-positions endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/positions", "POST", 201)
class PositionByQuote(Trading):
    """Create a new position by accepting a quote.

    See: docs/api/trading/positions.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(PositionByQuote, self).__init__()
        self.data = data


@endpoint("openapi/trade/v1/positions/{PositionId}", "PATCH", 204)
class UpdatePosition(Trading):
    """Update properties of an existing position.

    See: docs/api/trading/positions.md
    """

    def __init__(self, PositionId: str, data: dict[str, Any]) -> None:
        super(UpdatePosition, self).__init__(PositionId=PositionId)
        self.data = data


@endpoint("openapi/trade/v1/positions/{PositionId}/exercise", "PUT", 204)
class ExercisePosition(Trading):
    """Force exercise of a position.

    See: docs/api/trading/positions.md
    """

    def __init__(self, PositionId: str, data: dict[str, Any]) -> None:
        super(ExercisePosition, self).__init__(PositionId=PositionId)
        self.data = data


@endpoint("openapi/trade/v1/positions/exercise", "PUT", 204)
class ExerciseAmount(Trading):
    """Force exercise of an amount across all positions.

    See: docs/api/trading/positions.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(ExerciseAmount, self).__init__()
        self.data = data
