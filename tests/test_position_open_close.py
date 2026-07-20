"""Unit tests for PositionOpen / PositionClose body shapes and misuse guards."""

from __future__ import annotations

from unittest.mock import patch

import pytest
import saxo_api_client.definitions.orders as OD
from saxo_api_client.contrib.client import SaxoClient
from saxo_api_client.contrib.orders import PositionClose, PositionOpen, tie_account_to_order


class TestPositionOpen:
    def test_market_requires_is_force_open(self) -> None:
        with pytest.raises(TypeError, match="is_force_open"):
            PositionOpen.market(  # type: ignore[call-arg]
                uic=42,
                amount=10000,
                asset_type=OD.AssetType.FxSpot,
                buy_sell="Buy",
            )

    def test_market_force_open_true(self) -> None:
        order = PositionOpen.market(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Buy",
            is_force_open=True,
        )
        assert order.mode == "market"
        data = order.data
        assert data["OrderType"] == OD.OrderType.Market
        assert data["IsForceOpen"] is True
        assert data["BuySell"] == "Buy"
        assert data["Amount"] == 10000
        assert "PositionId" not in data

    def test_limit_and_stop_bodies(self) -> None:
        limit = PositionOpen.limit(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
            order_price=150.0,
            is_force_open=False,
        )
        assert limit.mode == "limit"
        assert limit.data["OrderType"] == OD.OrderType.Limit
        assert limit.data["OrderPrice"] == 150.0
        assert limit.data["BuySell"] == "Sell"
        assert limit.data["IsForceOpen"] is False

        stop = PositionOpen.stop(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Buy",
            order_price=149.0,
            is_force_open=True,
        )
        assert stop.mode == "stop"
        assert stop.data["OrderType"] == OD.OrderType.Stop
        assert stop.data["OrderPrice"] == 149.0

    def test_stop_limit_body(self) -> None:
        order = PositionOpen.stop_limit(
            uic=211,
            amount=1,
            asset_type=OD.AssetType.CfdOnStock,
            buy_sell="Sell",
            order_price=150.0,
            stop_limit_price=149.5,
            is_force_open=True,
        )
        assert order.mode == "stop_limit"
        assert order.data["OrderType"] == OD.OrderType.StopLimit
        assert order.data["StopLimitPrice"] == 149.5


class TestPositionClose:
    def test_fifo_market_has_no_position_id(self) -> None:
        order = PositionClose.fifo_market(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
        )
        assert order.mode == "fifo_market"
        data = order.data
        assert "PositionId" not in data
        assert "Orders" not in data
        assert data["IsForceOpen"] is False
        assert data["BuySell"] == "Sell"
        assert data["OrderType"] == OD.OrderType.Market
        assert data["ManualOrder"] is True

    def test_fifo_limit_and_stop(self) -> None:
        limit = PositionClose.fifo_limit(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
            order_price=150.25,
        )
        assert limit.mode == "fifo_limit"
        assert "PositionId" not in limit.data
        assert limit.data["OrderPrice"] == 150.25

        stop = PositionClose.fifo_stop(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
            order_price=149.5,
        )
        assert stop.mode == "fifo_stop"
        assert "PositionId" not in stop.data
        assert stop.data["OrderType"] == OD.OrderType.Stop

    def test_force_open_market_nested(self) -> None:
        order = PositionClose.force_open_market(
            position_id="POS-1",
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
        )
        assert order.mode == "force_open_market"
        data = order.data
        assert data["PositionId"] == "POS-1"
        assert len(data["Orders"]) == 1
        nested = data["Orders"][0]
        assert nested["OrderType"] == OD.OrderType.Market
        assert nested["BuySell"] == "Sell"
        assert nested["Amount"] == 10000
        assert nested["ManualOrder"] is True
        assert "IsForceOpen" not in nested

    def test_force_open_limit_and_stop_nested(self) -> None:
        limit = PositionClose.force_open_limit(
            position_id="POS-2",
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
            order_price=150.0,
        )
        assert limit.data["Orders"][0]["OrderType"] == OD.OrderType.Limit
        assert limit.data["Orders"][0]["OrderPrice"] == 150.0

        stop = PositionClose.force_open_stop(
            position_id="POS-3",
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
            order_price=150.0,
        )
        assert stop.mode == "force_open_stop"
        assert stop.data["Orders"][0]["OrderType"] == OD.OrderType.Stop
        assert stop.data["Orders"][0]["OrderPrice"] == 150.0

    def test_force_open_requires_position_id(self) -> None:
        with pytest.raises(TypeError, match="position_id"):
            PositionClose.force_open_market(  # type: ignore[call-arg]
                uic=42,
                amount=10000,
                asset_type=OD.AssetType.FxSpot,
                buy_sell="Sell",
            )

    def test_clear_force_open_market(self) -> None:
        order = PositionClose.clear_force_open_market(
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
        )
        assert order.mode == "clear_force_open"
        data = order.data
        assert data["ClearForceOpen"] is True
        assert data["OrderType"] == OD.OrderType.Market
        assert "PositionId" not in data

    def test_tie_account_injects_into_nested_orders(self) -> None:
        order = PositionClose.force_open_market(
            position_id="POS-1",
            uic=42,
            amount=10000,
            asset_type=OD.AssetType.FxSpot,
            buy_sell="Sell",
        )
        bound = tie_account_to_order("AK-TEST", order)
        assert "AccountKey" not in bound or bound.get("AccountKey") is None
        assert "AccountKey" not in bound  # top-level PositionId body: no AccountKey
        assert bound["Orders"][0]["AccountKey"] == "AK-TEST"
        assert bound["PositionId"] == "POS-1"

    def test_market_close_order_removed(self) -> None:
        with pytest.raises(ImportError):
            from saxo_api_client.contrib.orders import MarketCloseOrder  # noqa: F401


class TestSaxoClientFacade:
    def _client(self) -> SaxoClient:
        client = SaxoClient(access_token="dummy")
        client._account_key = "AK-TEST"
        return client

    def test_iter_open_positions_uses_top_level_position_id(self) -> None:
        client = self._client()
        payload = {
            "Data": [
                {
                    "PositionId": "TOP-LEVEL-ID",
                    "PositionBase": {
                        "Uic": 42,
                        "AssetType": "FxSpot",
                        "Amount": 10000,
                        "IsForceOpen": True,
                        "PositionId": "WRONG-NESTED",
                    },
                    "PositionView": {},
                }
            ]
        }
        with patch.object(client, "get_positions_query", return_value=payload):
            rows = client.iter_open_positions(uic=42)
        assert len(rows) == 1
        assert rows[0]["position_id"] == "TOP-LEVEL-ID"
        assert rows[0]["is_force_open"] is True
        assert rows[0]["buy_sell"] == "Buy"
        assert rows[0]["related_position_id"] is None
        assert rows[0]["status"] is None

    def test_iter_open_positions_exposes_related_and_status(self) -> None:
        client = self._client()
        payload = {
            "Data": [
                {
                    "PositionId": "REM-1",
                    "PositionBase": {
                        "Uic": 211,
                        "AssetType": "CfdOnIndex",
                        "Amount": 5,
                        "IsForceOpen": True,
                        "Status": "PartiallyClosed",
                        "RelatedPositionId": "ORIG-1",
                        "CanBeClosed": True,
                    },
                    "PositionView": {},
                }
            ]
        }
        with patch.object(client, "get_positions_query", return_value=payload):
            rows = client.iter_open_positions(uic=211)
        assert rows[0]["related_position_id"] == "ORIG-1"
        assert rows[0]["status"] == "PartiallyClosed"
        assert rows[0]["can_be_closed"] is True

    def test_open_market_rejects_stock_option(self) -> None:
        client = self._client()
        with pytest.raises(ValueError, match="OptionTrader"):
            client.open_market(
                asset_type=OD.AssetType.StockOption,
                uic=1,
                amount=1,
                buy_sell="Buy",
                is_force_open=False,
            )

    def test_close_force_open_rejects_stock_option(self) -> None:
        client = self._client()
        with pytest.raises(ValueError, match="OptionTrader"):
            client.close_force_open_market(
                position_id="POS-1",
                asset_type=OD.AssetType.StockOption,
                uic=1,
                amount=1,
                buy_sell="Sell",
                verify_position=False,
            )

    def test_resolve_force_open_close_target_follows_related(self) -> None:
        client = self._client()
        rows = [
            {
                "position_id": "REM-9",
                "uic": 211,
                "asset_type": "CfdOnIndex",
                "amount": 5.0,
                "buy_sell": "Buy",
                "is_force_open": True,
                "related_position_id": "ORIG-1",
                "status": "Open",
            }
        ]
        with patch.object(client, "iter_open_positions", return_value=rows):
            target = client.resolve_force_open_close_target(
                previous_position_id="ORIG-1",
                uic=211,
                asset_type="CfdOnIndex",
            )
        assert target is not None
        assert target["position_id"] == "REM-9"

    def test_resolve_force_open_close_target_none_when_flat(self) -> None:
        client = self._client()
        with patch.object(client, "iter_open_positions", return_value=[]):
            target = client.resolve_force_open_close_target(
                previous_position_id="GONE",
                uic=211,
            )
        assert target is None

    def test_close_force_open_market_places_nested_builder(self) -> None:
        client = self._client()
        fo_row = {
            "position_id": "POS-1",
            "uic": 42,
            "asset_type": "FxSpot",
            "amount": 10000.0,
            "buy_sell": "Buy",
            "is_force_open": True,
        }
        with (
            patch.object(client, "iter_open_positions", return_value=[fo_row]),
            patch.object(client, "_execute_order", return_value={"OrderId": "1"}) as exec_mock,
        ):
            client.close_force_open_market(
                position_id="POS-1",
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "force_open_market"
        assert placed.data["PositionId"] == "POS-1"

    def test_close_force_open_rejects_non_force_open(self) -> None:
        client = self._client()
        row = {
            "position_id": "POS-1",
            "is_force_open": False,
            "amount": 10000.0,
            "buy_sell": "Buy",
        }
        with (
            patch.object(client, "iter_open_positions", return_value=[row]),
            pytest.raises(ValueError, match="not ForceOpen"),
        ):
            client.close_force_open_market(
                position_id="POS-1",
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
            )

    def test_open_market_requires_is_force_open(self) -> None:
        client = self._client()
        with pytest.raises(TypeError, match="is_force_open"):
            client.open_market(  # type: ignore[call-arg]
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Buy",
            )

    def test_flatten_force_open_skipped_when_flat(self) -> None:
        client = self._client()
        with patch.object(client, "iter_open_positions", return_value=[]):
            out = client.flatten_force_open(asset_type="FxSpot", uic=42)
        assert out["skipped"] is True

    def test_flatten_force_open_places_clear(self) -> None:
        client = self._client()
        rows = [
            {
                "position_id": "A",
                "uic": 42,
                "asset_type": "FxSpot",
                "amount": 10000.0,
                "is_force_open": True,
            }
        ]
        with (
            patch.object(client, "iter_open_positions", return_value=rows),
            patch.object(client, "_execute_order", return_value={"OrderId": "9"}) as exec_mock,
        ):
            out = client.flatten_force_open(asset_type="FxSpot", uic=42)
        assert out["skipped"] is False
        assert out["buy_sell"] == "Sell"
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "clear_force_open"
        assert placed.data["ClearForceOpen"] is True

    def test_open_limit_and_stop_place_builders(self) -> None:
        client = self._client()
        with patch.object(client, "_execute_order", return_value={"OrderId": "1"}) as exec_mock:
            client.open_limit(
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Buy",
                order_price=150.0,
                is_force_open=True,
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "limit"
        assert placed.data["IsForceOpen"] is True
        assert placed.data["OrderPrice"] == 150.0

        with patch.object(client, "_execute_order", return_value={"OrderId": "2"}) as exec_mock:
            client.open_stop(
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
                order_price=149.0,
                is_force_open=False,
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "stop"
        assert placed.data["IsForceOpen"] is False

    def test_close_fifo_market_places_builder(self) -> None:
        client = self._client()
        with patch.object(client, "_execute_order", return_value={"OrderId": "3"}) as exec_mock:
            client.close_fifo_market(
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "fifo_market"
        assert "PositionId" not in placed.data

    def test_close_force_open_limit_and_stop(self) -> None:
        client = self._client()
        fo_row = {
            "position_id": "POS-1",
            "uic": 42,
            "asset_type": "FxSpot",
            "amount": 10000.0,
            "buy_sell": "Buy",
            "is_force_open": True,
        }
        with (
            patch.object(client, "iter_open_positions", return_value=[fo_row]),
            patch.object(client, "_execute_order", return_value={"OrderId": "4"}) as exec_mock,
        ):
            client.close_force_open_limit(
                position_id="POS-1",
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
                order_price=150.0,
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "force_open_limit"
        assert placed.data["Orders"][0]["OrderPrice"] == 150.0

        with (
            patch.object(client, "iter_open_positions", return_value=[fo_row]),
            patch.object(client, "_execute_order", return_value={"OrderId": "5"}) as exec_mock,
        ):
            client.close_force_open_stop(
                position_id="POS-1",
                asset_type="FxSpot",
                uic=42,
                amount=10000,
                buy_sell="Sell",
                order_price=149.5,
            )
        placed = exec_mock.call_args[0][0]
        assert placed.mode == "force_open_stop"
        assert placed.data["Orders"][0]["OrderType"] == OD.OrderType.Stop

    def test_summarize_client_netting_end_of_day_and_force_default(self) -> None:
        client = self._client()
        payload = {
            "ForceOpenDefaultValue": True,
            "PositionNettingMethod": "FIFO",
            "PositionNettingMode": "EndOfDay",
            "PositionNettingProfile": "FifoEndOfDay",
            "AllowedNettingProfiles": ["FifoEndOfDay"],
        }
        with patch.object(client, "get_client_details", return_value=payload):
            summary = client.summarize_client_netting()
        assert summary["position_netting_mode"] == "EndOfDay"
        assert summary["force_open_default_value"] is True
        assert summary["raw"] is payload
        joined = " ".join(summary["notes"])
        assert "not by account netting" in joined
        assert "EndOfDay" in joined and "zombie" in joined.lower()
        assert "ForceOpenDefaultValue is True" in joined

    def test_summarize_client_netting_intraday_minimal_notes(self) -> None:
        client = self._client()
        payload = {
            "ForceOpenDefaultValue": False,
            "PositionNettingMode": "Intraday",
            "PositionNettingProfile": "FifoRealTime",
            "PositionNettingMethod": "FIFO",
        }
        with patch.object(client, "get_client_details", return_value=payload):
            summary = client.summarize_client_netting()
        assert len(summary["notes"]) == 1
        assert "not by account netting" in summary["notes"][0]
