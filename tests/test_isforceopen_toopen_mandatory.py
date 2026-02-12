"""
IsForceOpen および ToOpenClose パラメータの必須化検証テスト

このテストは以下を検証します：
1. 注文クラスの IsForceOpen パラメータの動作（デフォルト値の確認）
2. OptionTrader の to_open_close パラメータの必須性
3. 正常系：適切なパラメータ指定時の動作
"""

import pytest
from unittest.mock import MagicMock, patch

import saxo_openapi.definitions.orders as OD
from saxo_openapi.contrib.orders import (
    MarketOrder,
    LimitOrder,
    StopOrder,
    StopLimitOrder,
    StopIfTradedOrder,
)
from saxo_openapi.contrib.option_trader import OptionTrader


class TestOrderIsForceOpenParameter:
    """注文クラスの IsForceOpen パラメータのテスト"""

    def test_market_order_default_isforceopen(self):
        """MarketOrder: デフォルトで IsForceOpen=True になることを確認"""
        order = MarketOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
        )
        assert order.data["IsForceOpen"] is True

    def test_market_order_isforceopen_false(self):
        """MarketOrder: IsForceOpen=False を明示的に指定（FIFOモード）"""
        order = MarketOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            IsForceOpen=False,
        )
        assert order.data["IsForceOpen"] is False

    def test_market_order_isforceopen_true(self):
        """MarketOrder: IsForceOpen=True を明示的に指定（両建てモード）"""
        order = MarketOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            IsForceOpen=True,
        )
        assert order.data["IsForceOpen"] is True

    def test_limit_order_default_isforceopen(self):
        """LimitOrder: デフォルトで IsForceOpen=True になることを確認"""
        order = LimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
        )
        assert order.data["IsForceOpen"] is True

    def test_limit_order_isforceopen_false(self):
        """LimitOrder: IsForceOpen=False を明示的に指定（FIFOモード）"""
        order = LimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
            IsForceOpen=False,
        )
        assert order.data["IsForceOpen"] is False

    def test_limit_order_isforceopen_true(self):
        """LimitOrder: IsForceOpen=True を明示的に指定（両建てモード）"""
        order = LimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
            IsForceOpen=True,
        )
        assert order.data["IsForceOpen"] is True

    def test_stop_order_default_isforceopen(self):
        """StopOrder: デフォルトで IsForceOpen=True になることを確認"""
        order = StopOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=55.0,
        )
        assert order.data["IsForceOpen"] is True

    def test_stop_order_isforceopen_false(self):
        """StopOrder: IsForceOpen=False を明示的に指定（FIFOモード）"""
        order = StopOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=55.0,
            IsForceOpen=False,
        )
        assert order.data["IsForceOpen"] is False

    def test_stop_limit_order_default_isforceopen(self):
        """StopLimitOrder: デフォルトで IsForceOpen=True になることを確認"""
        order = StopLimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
            StopLimitPrice=55.0,
        )
        assert order.data["IsForceOpen"] is True

    def test_stop_limit_order_isforceopen_false(self):
        """StopLimitOrder: IsForceOpen=False を明示的に指定（FIFOモード）"""
        order = StopLimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
            StopLimitPrice=55.0,
            IsForceOpen=False,
        )
        assert order.data["IsForceOpen"] is False

    def test_stop_if_traded_order_default_isforceopen(self):
        """StopIfTradedOrder: デフォルトで IsForceOpen=True になることを確認"""
        order = StopIfTradedOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=55.0,
        )
        assert order.data["IsForceOpen"] is True

    def test_stop_if_traded_order_isforceopen_false(self):
        """StopIfTradedOrder: IsForceOpen=False を明示的に指定（FIFOモード）"""
        order = StopIfTradedOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=55.0,
            IsForceOpen=False,
        )
        assert order.data["IsForceOpen"] is False


class TestOptionTraderToOpenCloseParameter:
    """OptionTrader の to_open_close パラメータのテスト"""

    def setup_method(self):
        """各テストの前にモッククライアントを準備"""
        self.mock_client = MagicMock()
        self.mock_client.request.return_value = {"OrderId": "TEST123"}
        self.trader = OptionTrader(self.mock_client, account_key="TEST_ACCOUNT")

    def test_buy_option_missing_to_open_close(self):
        """buy_option: to_open_close が指定されていない場合、TypeError が発生"""
        with pytest.raises(TypeError, match="to_open_close"):
            self.trader.buy_option(
                uic=12345,
                amount=1,
                order_type="Limit",
                order_price=3.50,
                # to_open_close を意図的に省略
            )

    def test_buy_option_with_to_open_close_to_open(self):
        """buy_option: to_open_close="ToOpen" を指定して正常に動作"""
        result = self.trader.buy_option(
            uic=12345,
            amount=1,
            to_open_close="ToOpen",
            order_type="Limit",
            order_price=3.50,
        )
        assert result["OrderId"] == "TEST123"

        # リクエストが呼ばれたことを確認
        assert self.mock_client.request.called
        call_args = self.mock_client.request.call_args[0][0]
        assert call_args.data["ToOpenClose"] == "ToOpen"
        assert call_args.data["BuySell"] == OD.BuySell.Buy

    def test_buy_option_with_to_open_close_to_close(self):
        """buy_option: to_open_close="ToClose" を指定して正常に動作"""
        result = self.trader.buy_option(
            uic=12345,
            amount=1,
            to_open_close="ToClose",
            order_type="Limit",
            order_price=3.50,
        )
        assert result["OrderId"] == "TEST123"

        call_args = self.mock_client.request.call_args[0][0]
        assert call_args.data["ToOpenClose"] == "ToClose"

    def test_sell_option_missing_to_open_close(self):
        """sell_option: to_open_close が指定されていない場合、TypeError が発生"""
        with pytest.raises(TypeError, match="to_open_close"):
            self.trader.sell_option(
                uic=12345,
                amount=1,
                order_type="Limit",
                order_price=3.50,
                # to_open_close を意図的に省略
            )

    def test_sell_option_with_to_open_close_to_open(self):
        """sell_option: to_open_close="ToOpen" を指定して正常に動作（新規売建）"""
        result = self.trader.sell_option(
            uic=12345,
            amount=1,
            to_open_close="ToOpen",
            order_type="Limit",
            order_price=3.50,
        )
        assert result["OrderId"] == "TEST123"

        call_args = self.mock_client.request.call_args[0][0]
        assert call_args.data["ToOpenClose"] == "ToOpen"
        assert call_args.data["BuySell"] == OD.BuySell.Sell

    def test_sell_option_with_to_open_close_to_close(self):
        """sell_option: to_open_close="ToClose" を指定して正常に動作（決済）"""
        result = self.trader.sell_option(
            uic=12345,
            amount=1,
            to_open_close="ToClose",
            order_type="Limit",
            order_price=3.50,
        )
        assert result["OrderId"] == "TEST123"

        call_args = self.mock_client.request.call_args[0][0]
        assert call_args.data["ToOpenClose"] == "ToClose"

    @patch.object(OptionTrader, "buy_option")
    def test_buy_call_missing_to_open_close(self, mock_buy_option):
        """buy_call: to_open_close が指定されていない場合、TypeError が発生"""
        # buy_option が呼ばれることを期待
        mock_buy_option.side_effect = TypeError("missing 1 required positional argument: 'to_open_close'")

        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            with pytest.raises(TypeError, match="to_open_close"):
                self.trader.buy_call(
                    keyword="AMD",
                    expiry_date="2026-02-06",
                    strike_price=240.0,
                    amount=1,
                    order_price=3.50,
                    # to_open_close を意図的に省略
                )

    def test_buy_call_with_to_open_close(self):
        """buy_call: to_open_close を指定して正常に動作"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            result = self.trader.buy_call(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                order_price=3.50,
            )
            assert result["OrderId"] == "TEST123"

    def test_buy_put_with_to_open_close(self):
        """buy_put: to_open_close を指定して正常に動作"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            result = self.trader.buy_put(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                order_price=3.50,
            )
            assert result["OrderId"] == "TEST123"

    def test_sell_call_with_to_open_close(self):
        """sell_call: to_open_close を指定して正常に動作"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            result = self.trader.sell_call(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                order_price=3.50,
            )
            assert result["OrderId"] == "TEST123"

    def test_sell_put_with_to_open_close(self):
        """sell_put: to_open_close を指定して正常に動作"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            result = self.trader.sell_put(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                order_price=3.50,
            )
            assert result["OrderId"] == "TEST123"

    def test_validate_order_with_to_open_close(self):
        """validate_order: to_open_close を指定して正常に動作"""
        result = self.trader.validate_order(
            uic=12345,
            amount=1,
            to_open_close="ToOpen",
            buy_sell="Buy",
            order_type="Limit",
            order_price=3.50,
        )
        assert result["OrderId"] == "TEST123"

    def test_create_leg_with_to_open_close(self):
        """create_leg: to_open_close を指定してレグ辞書を作成"""
        leg = self.trader.create_leg(
            uic=12345,
            amount=1,
            buy_sell="Buy",
            to_open_close="ToOpen",
        )
        assert leg["Uic"] == 12345
        assert leg["ToOpenClose"] == "ToOpen"
        assert leg["BuySell"] == "Buy"

    def test_create_call_leg_with_to_open_close(self):
        """create_call_leg: to_open_close を指定してCallレグを作成"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            leg = self.trader.create_call_leg(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                action="Buy",
            )
            assert leg["Uic"] == 12345
            assert leg["ToOpenClose"] == "ToOpen"
            assert leg["BuySell"] == "Buy"

    def test_create_put_leg_with_to_open_close(self):
        """create_put_leg: to_open_close を指定してPutレグを作成"""
        with patch.object(self.trader.finder, "find_option") as mock_find:
            mock_find.return_value = MagicMock(uic=12345)

            leg = self.trader.create_put_leg(
                keyword="AMD",
                expiry_date="2026-02-06",
                strike_price=240.0,
                amount=1,
                to_open_close="ToOpen",
                action="Sell",
            )
            assert leg["Uic"] == 12345
            assert leg["ToOpenClose"] == "ToOpen"
            assert leg["BuySell"] == "Sell"


class TestOrderDataStructure:
    """注文データ構造の検証テスト"""

    def test_market_order_data_structure_with_isforceopen(self):
        """MarketOrder: 生成されたデータ構造に IsForceOpen が含まれることを確認"""
        order = MarketOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            IsForceOpen=False,
        )

        data = order.data
        assert "IsForceOpen" in data
        assert data["IsForceOpen"] is False
        assert data["Uic"] == 12345
        assert data["Amount"] == 100
        assert data["AssetType"] == OD.AssetType.Stock
        assert data["OrderType"] == OD.OrderType.Market

    def test_limit_order_data_structure_with_isforceopen(self):
        """LimitOrder: 生成されたデータ構造に IsForceOpen が含まれることを確認"""
        order = LimitOrder(
            Uic=12345,
            Amount=100,
            AssetType=OD.AssetType.Stock,
            OrderPrice=50.0,
            IsForceOpen=True,
        )

        data = order.data
        assert "IsForceOpen" in data
        assert data["IsForceOpen"] is True
        assert data["OrderPrice"] == 50.0
        assert data["OrderType"] == OD.OrderType.Limit

    def test_option_trader_order_structure_with_to_open_close(self):
        """OptionTrader: 生成されたオプション注文に ToOpenClose が含まれることを確認"""
        mock_client = MagicMock()
        trader = OptionTrader(mock_client, account_key="TEST_ACCOUNT")

        # _build_option_order メソッドを直接テスト
        order_spec = trader._build_option_order(
            uic=12345,
            amount=1,
            buy_sell=OD.BuySell.Buy,
            order_type="Limit",
            asset_type="StockOption",
            to_open_close="ToOpen",
            order_price=3.50,
        )

        assert "ToOpenClose" in order_spec
        assert order_spec["ToOpenClose"] == "ToOpen"
        assert order_spec["Uic"] == 12345
        assert order_spec["BuySell"] == OD.BuySell.Buy
        assert order_spec["OrderType"] == "Limit"
        assert order_spec["OrderPrice"] == 3.50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
