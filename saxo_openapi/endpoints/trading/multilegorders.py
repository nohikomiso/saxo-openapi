"""Handle trading multileg orders endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Trading


@endpoint("openapi/trade/v2/orders/multileg", "POST", 200)
class MultilegOrder(Trading):
    """Place a multileg order.

    See: docs/api/trading/orders.md#multilegorder
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(MultilegOrder, self).__init__()
        self.data = data


@endpoint("openapi/trade/v2/orders/multileg/precheck", "POST", 200)
class MultilegOrderPrecheck(Trading):
    """Precheck a multileg order.

    See: docs/api/trading/orders.md#multilegorderprecheck
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(MultilegOrderPrecheck, self).__init__()
        self.data = data


@endpoint("openapi/trade/v2/orders/multileg/defaults")
class MultilegOrderDefaults(Trading):
    """Get multileg order defaults.

    See: docs/api/trading/orders.md#multilegorderdefaults
    """

    def __init__(self, params: dict[str, Any] | None = None) -> None:
        super(MultilegOrderDefaults, self).__init__()
        self.params = params


@endpoint("openapi/trade/v2/orders/multileg", "PATCH", 200)
class ChangeMultilegOrder(Trading):
    """Change an existing multileg order.

    See: docs/api/trading/orders.md#changemultilegorder
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(ChangeMultilegOrder, self).__init__()
        self.data = data


@endpoint("openapi/trade/v2/orders/multileg/{MultiLegOrderId}", "DELETE", 200)
class CancelMultilegOrder(Trading):
    """Cancel a multileg order.

    See: docs/api/trading/orders.md#cancelmultilegorder
    """

    def __init__(self, MultiLegOrderId: str, params: dict[str, Any] | None = None) -> None:
        super(CancelMultilegOrder, self).__init__(MultiLegOrderId=MultiLegOrderId)
        self.params = params
