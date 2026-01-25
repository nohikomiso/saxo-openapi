# -*- encoding: utf-8 -*-

"""Handle chart-charts endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Charts


@endpoint("openapi/chart/v3/charts")  # v1からv3に変更
class GetChartData(Charts):
    """Return chart data as specified by request parameters.

    See: `docs/api/chart/charts.md#getchartdata`
    """

    def __init__(self, params: dict[str, Any]) -> None:
        """Instantiate a GetChartData request."""
        super(GetChartData, self).__init__()
        self.params = params


@endpoint("openapi/chart/v3/charts/subscriptions", "POST", 201)  # v1からv3に変更
class CreateChartDataSubscription(Charts):
    """Sets up a subscription and returns an initial snapshot of most recently
    completed samples specified by the parameters in the request.

    Subsequent samples are delivered over the streaming channel. Most often
    a single new sample or sample update is delivered at a time, but when a
    sample closes, you will typcially get two samples: The now closed bar, and
    the bar just opening.

    See: `docs/api/chart/charts.md#createchartdatasubscription`
    """

    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, data: dict[str, Any]) -> None:
        """Instantiate a CreateChartDataSubscription request."""
        super(CreateChartDataSubscription, self).__init__()
        self.data = data


@endpoint(
    "openapi/chart/v3/charts/subscriptions/{ContextId}", "DELETE", 202
)  # v1からv3に変更
class ChartDataRemoveSubscriptions(Charts):
    """Removes all subscriptions for the current session on this resource, and
    frees all resources on the server.

    See: `docs/api/chart/charts.md#chartdataremovesubscriptions`
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any] | None = None) -> None:
        """Instantiate a ChartDataRemoveSubscriptions request."""
        super(ChartDataRemoveSubscriptions, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint(
    "openapi/chart/v3/charts/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 202
)  # v1からv3に変更
class ChartDataRemoveSubscription(Charts):
    """Removes subscriptions for the given reference id on this resource, and
    frees resources on the server.

    See: `docs/api/chart/charts.md#chartdataremovesubscription`
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        """Instantiate a ChartDataRemoveSubscription request."""
        super(ChartDataRemoveSubscription, self).__init__(
            ContextId=ContextId, ReferenceId=ReferenceId
        )
