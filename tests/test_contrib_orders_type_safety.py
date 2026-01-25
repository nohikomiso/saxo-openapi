"""Test type safety improvements for contrib orders module.

Tests verify that:
1. All order classes' __init__ methods have type hints
2. Type hints are correctly applied to key parameters (Uic, Amount, AssetType, BuySell)
3. Order instances can be created and return valid data
4. Import statements work correctly
"""

import inspect
import json

import pytest
import saxo_openapi.definitions.orders as OD
from saxo_openapi.contrib.orders import (
    LimitOrder,
    LimitOrderFxSpot,
    LimitOrderStock,
    MarketOrder,
    MarketOrderCfdOnStock,
    MarketOrderFxSpot,
    MarketOrderStock,
    StopIfTradedOrder,
    StopIfTradedOrderCfdOnStock,
    StopLimitOrder,
    StopLimitOrderCfdOnStock,
    StopOrder,
    StopOrderFxSpot,
)
from saxo_openapi.contrib.orders.baseorder import BaseOrder
from saxo_openapi.contrib.orders.helper import (
    direction_from_amount,
    direction_invert,
    order_duration_spec,
    tie_account_to_order,
)
from saxo_openapi.contrib.orders.mixin import OnFillHnd
from saxo_openapi.contrib.orders.onfill import (
    OnFill,
    StopLossDetails,
    TakeProfitDetails,
)
from saxo_openapi.types.primitives import AssetType, Uic


class TestTypeHints:
    """Test that __init__ methods have proper type hints."""

    def test_market_order_has_type_hints(self):
        """MarketOrder.__init__ should have type hints."""
        sig = inspect.signature(MarketOrder.__init__)
        params = sig.parameters
        # Check critical parameters have annotations
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["AssetType"].annotation != inspect.Parameter.empty

    def test_market_order_stock_has_type_hints(self):
        """MarketOrderStock.__init__ should have type hints."""
        sig = inspect.signature(MarketOrderStock.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty

    def test_market_order_cfd_on_stock_has_type_hints(self):
        """MarketOrderCfdOnStock.__init__ should have type hints."""
        sig = inspect.signature(MarketOrderCfdOnStock.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty

    def test_market_order_fx_spot_has_type_hints(self):
        """MarketOrderFxSpot.__init__ should have type hints."""
        sig = inspect.signature(MarketOrderFxSpot.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty

    def test_limit_order_has_type_hints(self):
        """LimitOrder.__init__ should have type hints."""
        sig = inspect.signature(LimitOrder.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["AssetType"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_limit_order_stock_has_type_hints(self):
        """LimitOrderStock.__init__ should have type hints."""
        sig = inspect.signature(LimitOrderStock.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_limit_order_fx_spot_has_type_hints(self):
        """LimitOrderFxSpot.__init__ should have type hints."""
        sig = inspect.signature(LimitOrderFxSpot.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_stop_order_has_type_hints(self):
        """StopOrder.__init__ should have type hints."""
        sig = inspect.signature(StopOrder.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["AssetType"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_stop_order_fx_spot_has_type_hints(self):
        """StopOrderFxSpot.__init__ should have type hints."""
        sig = inspect.signature(StopOrderFxSpot.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_stop_limit_order_has_type_hints(self):
        """StopLimitOrder.__init__ should have type hints."""
        sig = inspect.signature(StopLimitOrder.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["AssetType"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty
        assert params["StopLimitPrice"].annotation != inspect.Parameter.empty

    def test_stop_limit_order_cfd_on_stock_has_type_hints(self):
        """StopLimitOrderCfdOnStock.__init__ should have type hints."""
        sig = inspect.signature(StopLimitOrderCfdOnStock.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty
        assert params["StopLimitPrice"].annotation != inspect.Parameter.empty

    def test_stop_if_traded_order_has_type_hints(self):
        """StopIfTradedOrder.__init__ should have type hints."""
        sig = inspect.signature(StopIfTradedOrder.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["AssetType"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_stop_if_traded_order_cfd_on_stock_has_type_hints(self):
        """StopIfTradedOrderCfdOnStock.__init__ should have type hints."""
        sig = inspect.signature(StopIfTradedOrderCfdOnStock.__init__)
        params = sig.parameters
        assert params["Uic"].annotation != inspect.Parameter.empty
        assert params["Amount"].annotation != inspect.Parameter.empty
        assert params["OrderPrice"].annotation != inspect.Parameter.empty

    def test_base_order_abstract_init(self):
        """BaseOrder.__init__ should be abstract."""
        # Should not be instantiable directly
        with pytest.raises(TypeError):
            BaseOrder()

    def test_on_fill_abstract_init(self):
        """OnFill.__init__ should be abstract."""
        # Should not be instantiable directly
        with pytest.raises(TypeError):
            OnFill(OrderType=OD.OrderType.Limit)


class TestOrderCreation:
    """Test that orders can be created with proper type hints."""

    def test_market_order_creation(self):
        """MarketOrder should be creatable with type-safe parameters."""
        order = MarketOrder(
            Uic=21,
            Amount=10000,
            AssetType=OD.AssetType.FxSpot,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["Amount"] == 10000
        assert data["AssetType"] == OD.AssetType.FxSpot
        assert data["BuySell"] == OD.Direction.Buy

    def test_market_order_stock_creation(self):
        """MarketOrderStock should be creatable."""
        order = MarketOrderStock(
            Uic=16350,
            Amount=100,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 16350
        assert data["AssetType"] == OD.AssetType.Stock
        assert data["BuySell"] == OD.Direction.Buy

    def test_market_order_cfd_on_stock_creation(self):
        """MarketOrderCfdOnStock should be creatable."""
        order = MarketOrderCfdOnStock(
            Uic=211,
            Amount=10,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 211
        assert data["AssetType"] == OD.AssetType.CfdOnStock

    def test_market_order_fx_spot_creation(self):
        """MarketOrderFxSpot should be creatable."""
        order = MarketOrderFxSpot(
            Uic=21,
            Amount=50000,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["AssetType"] == OD.AssetType.FxSpot
        assert data["Amount"] == 50000

    def test_limit_order_creation(self):
        """LimitOrder should be creatable."""
        order = LimitOrder(
            Uic=21,
            Amount=10000,
            AssetType=OD.AssetType.FxSpot,
            OrderPrice=1.1025,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["Amount"] == 10000
        assert data["OrderPrice"] == 1.1025
        assert data["BuySell"] == OD.Direction.Buy

    def test_limit_order_stock_creation(self):
        """LimitOrderStock should be creatable."""
        order = LimitOrderStock(
            Uic=16350,
            Amount=100,
            OrderPrice=28.00,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 16350
        assert data["AssetType"] == OD.AssetType.Stock
        assert data["OrderPrice"] == 28.00

    def test_limit_order_fx_spot_creation(self):
        """LimitOrderFxSpot should be creatable."""
        order = LimitOrderFxSpot(
            Uic=21,
            Amount=25000,
            OrderPrice=1.1025,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["AssetType"] == OD.AssetType.FxSpot

    def test_stop_order_creation(self):
        """StopOrder should be creatable."""
        order = StopOrder(
            Uic=21,
            Amount=10000,
            AssetType=OD.AssetType.FxSpot,
            OrderPrice=1.1000,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["OrderPrice"] == 1.1000

    def test_stop_order_fx_spot_creation(self):
        """StopOrderFxSpot should be creatable."""
        order = StopOrderFxSpot(
            Uic=21,
            Amount=25000,
            OrderPrice=1.1025,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 21
        assert data["AssetType"] == OD.AssetType.FxSpot

    def test_stop_limit_order_creation(self):
        """StopLimitOrder should be creatable."""
        order = StopLimitOrder(
            Uic=211,
            Amount=1,
            AssetType=OD.AssetType.CfdOnStock,
            OrderPrice=150.0,
            StopLimitPrice=149.5,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 211
        assert data["OrderPrice"] == 150.0
        assert data["StopLimitPrice"] == 149.5

    def test_stop_limit_order_cfd_on_stock_creation(self):
        """StopLimitOrderCfdOnStock should be creatable."""
        order = StopLimitOrderCfdOnStock(
            Uic=211,
            Amount=1,
            OrderPrice=150.0,
            StopLimitPrice=149.5,
        )
        assert order is not None
        data = order.data
        assert data["AssetType"] == OD.AssetType.CfdOnStock

    def test_stop_if_traded_order_creation(self):
        """StopIfTradedOrder should be creatable."""
        order = StopIfTradedOrder(
            Uic=211,
            Amount=1,
            AssetType=OD.AssetType.CfdOnStock,
            OrderPrice=150.0,
        )
        assert order is not None
        data = order.data
        assert data["Uic"] == 211
        assert data["OrderPrice"] == 150.0

    def test_stop_if_traded_order_cfd_on_stock_creation(self):
        """StopIfTradedOrderCfdOnStock should be creatable."""
        order = StopIfTradedOrderCfdOnStock(
            Uic=211,
            Amount=1,
            OrderPrice=150.0,
        )
        assert order is not None
        data = order.data
        assert data["AssetType"] == OD.AssetType.CfdOnStock


class TestHelperFunctions:
    """Test helper functions work correctly."""

    def test_direction_from_amount_buy(self):
        """direction_from_amount should return Buy for positive amounts."""
        result = direction_from_amount(100)
        assert result == OD.Direction.Buy

    def test_direction_from_amount_sell(self):
        """direction_from_amount should return Sell for negative amounts."""
        result = direction_from_amount(-100)
        assert result == OD.Direction.Sell

    def test_direction_invert(self):
        """direction_invert should flip Buy to Sell and vice versa."""
        assert direction_invert(OD.Direction.Buy) == OD.Direction.Sell
        assert direction_invert(OD.Direction.Sell) == OD.Direction.Buy

    def test_tie_account_to_order_dict(self):
        """tie_account_to_order should add AccountKey to order dict."""
        order_dict = {
            "Uic": 21,
            "AssetType": "FxSpot",
            "Amount": 10000,
        }
        result = tie_account_to_order("test_account_key", order_dict)
        assert result["AccountKey"] == "test_account_key"

    def test_tie_account_to_order_instance(self):
        """tie_account_to_order should add AccountKey to order instance."""
        order = MarketOrderFxSpot(Uic=21, Amount=10000)
        result = tie_account_to_order("test_account_key", order)
        assert result["AccountKey"] == "test_account_key"


class TestOrderDataStructure:
    """Test that order data structures are valid."""

    def test_market_order_data_json_serializable(self):
        """Order data should be JSON serializable."""
        order = MarketOrderFxSpot(Uic=21, Amount=10000)
        data = order.data
        json_str = json.dumps(data)
        assert json_str is not None
        loaded = json.loads(json_str)
        assert loaded["Uic"] == 21

    def test_order_with_external_reference(self):
        """Orders should support ExternalReference parameter."""
        order = MarketOrderFxSpot(
            Uic=21,
            Amount=10000,
            ExternalReference="my_order_123",
        )
        data = order.data
        assert data["ExternalReference"] == "my_order_123"

    def test_order_with_on_fill_details(self):
        """Orders should support TakeProfit and StopLoss on fill."""
        tp = TakeProfitDetails(price=1.14)
        sl = StopLossDetails(price=1.12)
        order = MarketOrderFxSpot(
            Uic=21,
            Amount=10000,
            TakeProfitOnFill=tp,
            StopLossOnFill=sl,
        )
        data = order.data
        assert "Orders" in data
        assert len(data["Orders"]) == 2


class TestImports:
    """Test that all modules can be imported correctly."""

    def test_baseorder_import(self):
        """Should import BaseOrder."""
        assert BaseOrder is not None

    def test_mixin_import(self):
        """Should import OnFillHnd mixin."""
        assert OnFillHnd is not None

    def test_onfill_import(self):
        """Should import OnFill, TakeProfitDetails, StopLossDetails."""
        assert OnFill is not None
        assert TakeProfitDetails is not None
        assert StopLossDetails is not None

    def test_all_order_classes_import(self):
        """Should import all order classes."""
        assert MarketOrder is not None
        assert MarketOrderFxSpot is not None
        assert MarketOrderStock is not None
        assert MarketOrderCfdOnStock is not None
        assert LimitOrder is not None
        assert LimitOrderFxSpot is not None
        assert LimitOrderStock is not None
        assert StopOrder is not None
        assert StopOrderFxSpot is not None
        assert StopLimitOrder is not None
        assert StopLimitOrderCfdOnStock is not None
        assert StopIfTradedOrder is not None
        assert StopIfTradedOrderCfdOnStock is not None

    def test_helper_import(self):
        """Should import helper functions."""
        assert direction_from_amount is not None
        assert direction_invert is not None
        assert tie_account_to_order is not None
        assert order_duration_spec is not None

    def test_types_import(self):
        """Should import type definitions."""
        assert Uic is not None
        assert AssetType is not None
