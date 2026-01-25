"""Handle portfolio-balances endpoints."""

from typing import Any

from ..decorators import endpoint
from .base import Portfolio


@endpoint("openapi/port/v1/balances/me")
class AccountBalancesMe(Portfolio):
    """Get balance data for a client or an account.

    See: docs/api/portfolio/balances.md#accountbalancesme
    """

    def __init__(self) -> None:
        super(AccountBalancesMe, self).__init__()


@endpoint("openapi/port/v1/balances")
class AccountBalances(Portfolio):
    """Get balance data for a client, account group or an account.

    See: docs/api/portfolio/balances.md#accountbalances
    """

    def __init__(self, params: dict[str, Any]) -> None:
        super(AccountBalances, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/balances/marginoverview/")
class MarginOverview(Portfolio):
    """Get margin overview for a client, account group or an account.

    See: docs/api/portfolio/balances.md#marginoverview
    """

    def __init__(self, params: dict[str, Any]) -> None:
        super(MarginOverview, self).__init__()
        self.params = params


@endpoint("openapi/port/v1/balances/subscriptions", "POST", 201)
class BalanceSubscriptionCreate(Portfolio):
    """Set up a subscription and returns an initial snapshot of a balance.

    See: docs/api/portfolio/balances.md#balancesubscriptioncreate
    """

    def __init__(self, data: dict[str, Any]) -> None:
        super(BalanceSubscriptionCreate, self).__init__()
        self.data = data


@endpoint("openapi/port/v1/balances/subscriptions/{ContextId}", "DELETE", 201)
class BalanceSubscriptionRemoveByTag(Portfolio):
    """Remove multiple subscriptions for the current session.

    See: docs/api/portfolio/balances.md#balancesubscriptionremovebytag
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, params: dict[str, Any]) -> None:
        super(BalanceSubscriptionRemoveByTag, self).__init__(ContextId=ContextId)
        self.params = params


@endpoint("openapi/port/v1/balances/subscriptions/{ContextId}/{ReferenceId}", "DELETE", 201)
class BalanceSubscriptionRemoveById(Portfolio):
    """Removes subscription for the current session identified by subscription id.

    See: docs/api/portfolio/balances.md#balancesubscriptionremovebyid
    """

    RESPONSE_DATA = None

    def __init__(self, ContextId: str, ReferenceId: str) -> None:
        super(BalanceSubscriptionRemoveById, self).__init__(ContextId=ContextId, ReferenceId=ReferenceId)
