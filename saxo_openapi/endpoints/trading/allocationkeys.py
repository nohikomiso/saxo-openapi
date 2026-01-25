"""Handle trading-allocationkeys endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v1/allocationkeys", "GET")
class GetAllocationKeys(Trading):
    """Get a list of existing allocation keys.

    See: docs/api/trading/allocationkeys.md
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(GetAllocationKeys, self).__init__()
        self.params = params


@endpoint("openapi/trade/v1/allocationkeys/{AllocationKeyId}", "GET")
class GetAllocationKeyDetails(Trading):
    """Get detailed information about an allocation key.

    See: docs/api/trading/allocationkeys.md
    """

    def __init__(self, AllocationKeyId: str) -> None:
        super(GetAllocationKeyDetails, self).__init__(AllocationKeyId=AllocationKeyId)


@endpoint("openapi/trade/v1/allocationkeys", "POST", 201)
class CreateAllocationKey(Trading):
    """Create an allocation key.

    See: docs/api/trading/allocationkeys.md
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(CreateAllocationKey, self).__init__()
        self.data = data


@endpoint("openapi/trade/v1/allocationkeys/{AllocationKeyId}", "DELETE", 204)
class DeleteAllocationKey(Trading):
    """Delete an allocation key.

    See: docs/api/trading/allocationkeys.md
    """

    RESPONSE_DATA = None

    def __init__(self, AllocationKeyId: str) -> None:
        super(DeleteAllocationKey, self).__init__(AllocationKeyId=AllocationKeyId)


@endpoint("openapi/trade/v1/allocationkeys/distributions/{AllocationKeyId}")
class GetAllocationKeyDistributions(Trading):
    """Get distributions for an allocation key.

    See: docs/api/trading/allocationkeys.md#getallocationkeydistributions
    """

    def __init__(self, AllocationKeyId: str) -> None:
        super(GetAllocationKeyDistributions, self).__init__(AllocationKeyId=AllocationKeyId)
