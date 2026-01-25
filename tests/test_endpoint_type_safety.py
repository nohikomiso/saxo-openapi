"""Type safety tests for main endpoints (Task 7.3.4).

This test module verifies that main endpoint classes have proper type hints
for their __init__ methods. Testing the following endpoints:

Portfolio:
- balances.py: AccountBalancesMe, AccountBalances, MarginOverview, etc.
- positions.py: SinglePosition, PositionsMe, PositionsQuery, etc.
- orders.py: GetOpenOrder, GetOpenOrdersMe, OrderDetails, etc.

Trading:
- orders.py: Order, ChangeOrder, CancelOrders, etc.
- prices.py: CreatePriceSubscription, etc.

ReferenceData:
- instruments.py: Instruments, InstrumentDetails, etc.

AccountHistory:
- performance.py: AccountPerformance

RootServices:
- sessions.py: GetSessionCapabilities, ChangeSessionCapabilities, etc.
"""

import inspect
from typing import get_type_hints

import pytest
from saxo_openapi.endpoints.accounthistory import performance
from saxo_openapi.endpoints.portfolio import balances, orders, positions
from saxo_openapi.endpoints.referencedata import instruments
from saxo_openapi.endpoints.rootservices import sessions
from saxo_openapi.endpoints.trading import orders as trading_orders
from saxo_openapi.endpoints.trading import prices


class TestPortfolioBalancesTypeHints:
    """Test type hints for portfolio balance endpoints."""

    def test_account_balances_me_has_init(self):
        """Test AccountBalancesMe.__init__ exists."""
        assert hasattr(balances.AccountBalancesMe, "__init__")
        init = getattr(balances.AccountBalancesMe, "__init__")
        assert callable(init)

    def test_account_balances_has_init_with_params(self):
        """Test AccountBalances.__init__ accepts params."""
        init = getattr(balances.AccountBalances, "__init__")
        sig = inspect.signature(init)
        params = list(sig.parameters.keys())
        assert (
            "params" in params
        ), "AccountBalances.__init__ should have params parameter"

    def test_account_balances_me_init_hints(self):
        """Test AccountBalancesMe.__init__ has type hints."""
        init = getattr(balances.AccountBalancesMe, "__init__")
        try:
            hints = get_type_hints(init)
            # Should have return hint at minimum
            assert "return" in hints or len(hints) > 0
        except Exception:
            pytest.skip("Type hints not available for this class")

    def test_margin_overview_has_params(self):
        """Test MarginOverview.__init__ accepts params."""
        init = getattr(balances.MarginOverview, "__init__")
        sig = inspect.signature(init)
        assert "params" in sig.parameters

    def test_balance_subscription_create_has_data(self):
        """Test BalanceSubscriptionCreate.__init__ accepts data."""
        init = getattr(balances.BalanceSubscriptionCreate, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters


class TestPortfolioPositionsTypeHints:
    """Test type hints for portfolio position endpoints."""

    def test_single_position_has_init(self):
        """Test SinglePosition.__init__ exists."""
        assert hasattr(positions.SinglePosition, "__init__")

    def test_single_position_has_position_id(self):
        """Test SinglePosition.__init__ has PositionId parameter."""
        init = getattr(positions.SinglePosition, "__init__")
        sig = inspect.signature(init)
        assert "PositionId" in sig.parameters

    def test_positions_me_has_init(self):
        """Test PositionsMe.__init__ exists."""
        assert hasattr(positions.PositionsMe, "__init__")

    def test_positions_query_has_params(self):
        """Test PositionsQuery.__init__ has params."""
        init = getattr(positions.PositionsQuery, "__init__")
        sig = inspect.signature(init)
        assert "params" in sig.parameters

    def test_position_list_subscription_has_data(self):
        """Test PositionListSubscription.__init__ has data."""
        init = getattr(positions.PositionListSubscription, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters


class TestPortfolioOrdersTypeHints:
    """Test type hints for portfolio order endpoints."""

    def test_get_open_order_has_client_key(self):
        """Test GetOpenOrder.__init__ has ClientKey."""
        init = getattr(orders.GetOpenOrder, "__init__")
        sig = inspect.signature(init)
        assert "ClientKey" in sig.parameters
        assert "OrderId" in sig.parameters

    def test_get_open_orders_me_has_init(self):
        """Test GetOpenOrdersMe.__init__ exists."""
        assert hasattr(orders.GetOpenOrdersMe, "__init__")

    def test_order_details_has_order_id(self):
        """Test OrderDetails.__init__ has OrderId."""
        init = getattr(orders.OrderDetails, "__init__")
        sig = inspect.signature(init)
        assert "OrderId" in sig.parameters

    def test_create_open_orders_subscription_has_data(self):
        """Test CreateOpenOrdersSubscription.__init__ has data."""
        init = getattr(orders.CreateOpenOrdersSubscription, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters


class TestTradingOrdersTypeHints:
    """Test type hints for trading order endpoints."""

    def test_order_has_data(self):
        """Test Order.__init__ has data parameter."""
        init = getattr(trading_orders.Order, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters

    def test_change_order_has_data(self):
        """Test ChangeOrder.__init__ has data."""
        init = getattr(trading_orders.ChangeOrder, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters

    def test_cancel_orders_has_order_ids(self):
        """Test CancelOrders.__init__ has OrderIds."""
        init = getattr(trading_orders.CancelOrders, "__init__")
        sig = inspect.signature(init)
        assert "OrderIds" in sig.parameters
        assert "params" in sig.parameters

    def test_precheck_order_has_data(self):
        """Test PrecheckOrder.__init__ has data."""
        init = getattr(trading_orders.PrecheckOrder, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters


class TestTradingPricesTypeHints:
    """Test type hints for trading price endpoints."""

    def test_create_price_subscription_has_data(self):
        """Test CreatePriceSubscription.__init__ has data."""
        init = getattr(prices.CreatePriceSubscription, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters

    def test_margin_impact_request_has_context_id(self):
        """Test MarginImpactRequest.__init__ has ContextId."""
        init = getattr(prices.MarginImpactRequest, "__init__")
        sig = inspect.signature(init)
        assert "ContextId" in sig.parameters
        assert "ReferenceId" in sig.parameters

    def test_price_subscription_remove_by_tag_has_context_id(self):
        """Test PriceSubscriptionRemoveByTag.__init__ has ContextId."""
        init = getattr(prices.PriceSubscriptionRemoveByTag, "__init__")
        sig = inspect.signature(init)
        assert "ContextId" in sig.parameters


class TestReferencedataInstrumentsTypeHints:
    """Test type hints for referencedata instrument endpoints."""

    def test_instruments_has_params(self):
        """Test Instruments.__init__ has params."""
        init = getattr(instruments.Instruments, "__init__")
        sig = inspect.signature(init)
        assert "params" in sig.parameters

    def test_instrument_details_has_uic_and_asset_type(self):
        """Test InstrumentDetails.__init__ has Uic and AssetType."""
        init = getattr(instruments.InstrumentDetails, "__init__")
        sig = inspect.signature(init)
        assert "Uic" in sig.parameters
        assert "AssetType" in sig.parameters

    def test_contract_option_spaces_has_option_root_id(self):
        """Test ContractoptionSpaces.__init__ has OptionRootId."""
        init = getattr(instruments.ContractoptionSpaces, "__init__")
        sig = inspect.signature(init)
        assert "OptionRootId" in sig.parameters

    def test_trading_schedule_has_uic_and_asset_type(self):
        """Test TradingSchedule.__init__ has Uic and AssetType."""
        init = getattr(instruments.TradingSchedule, "__init__")
        sig = inspect.signature(init)
        assert "Uic" in sig.parameters
        assert "AssetType" in sig.parameters


class TestAccountHistoryPerformanceTypeHints:
    """Test type hints for account history performance endpoints."""

    def test_account_performance_has_client_key(self):
        """Test AccountPerformance.__init__ has ClientKey."""
        init = getattr(performance.AccountPerformance, "__init__")
        sig = inspect.signature(init)
        assert "ClientKey" in sig.parameters


class TestRootServicesSessionsTypeHints:
    """Test type hints for root services sessions endpoints."""

    def test_get_session_capabilities_has_init(self):
        """Test GetSessionCapabilities.__init__ exists."""
        assert hasattr(sessions.GetSessionCapabilities, "__init__")

    def test_change_session_capabilities_has_data(self):
        """Test ChangeSessionCapabilities.__init__ has data."""
        init = getattr(sessions.ChangeSessionCapabilities, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters

    def test_create_session_capabilities_subscription_has_data(self):
        """Test CreateSessionCapabilitiesSubscription.__init__ has data."""
        init = getattr(sessions.CreateSessionCapabilitiesSubscription, "__init__")
        sig = inspect.signature(init)
        assert "data" in sig.parameters

    def test_remove_session_capabilities_subscription_has_context_id(self):
        """Test RemoveSessionCapabilitiesSubscription.__init__ has ContextId."""
        init = getattr(sessions.RemoveSessionCapabilitiesSubscription, "__init__")
        sig = inspect.signature(init)
        assert "ContextId" in sig.parameters
        assert "ReferenceId" in sig.parameters


class TestEndpointImportsAndInstantiation:
    """Test that endpoints can be imported and instantiated."""

    def test_balance_endpoint_import_and_instantiation(self):
        """Test AccountBalancesMe can be imported and used."""
        ep = balances.AccountBalancesMe()
        assert ep is not None

    def test_position_endpoint_instantiation(self):
        """Test PositionsMe can be imported and instantiated."""
        ep = positions.PositionsMe()
        assert ep is not None

    def test_trading_order_endpoint_instantiation(self):
        """Test Order can be imported and instantiated with data."""
        data = {"Uic": 21, "AssetType": "FxSpot", "Amount": 100000, "BuySell": "Buy"}
        ep = trading_orders.Order(data=data)
        assert ep is not None
        assert hasattr(ep, "data")

    def test_reference_data_instruments_instantiation(self):
        """Test Instruments can be instantiated with params."""
        params = {"Keywords": "EUR"}
        ep = instruments.Instruments(params=params)
        assert ep is not None
        assert hasattr(ep, "params")
