"""ClientKey defaulting for PositionsQuery / GetAllOpenOrders."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from saxo_api_client.contrib.client import SaxoClient


def test_get_positions_query_fills_client_key_when_omitted() -> None:
    client = SaxoClient(access_token="dummy")
    client._client_key = "ck-from-cache"
    client._account_key = "ak-from-cache"
    captured: dict = {}

    def _request(cmd: object) -> dict:
        captured["params"] = getattr(cmd, "params", None)
        return {"Data": []}

    client._api = MagicMock()
    client._api.request.side_effect = _request

    client.get_positions_query()

    assert captured["params"]["ClientKey"] == "ck-from-cache"
    assert "AccountKey" not in captured["params"]


def test_get_positions_query_fetches_client_key_via_accounts_me() -> None:
    client = SaxoClient(access_token="dummy")
    captured: dict = {}

    def _request(cmd: object) -> dict:
        captured["params"] = getattr(cmd, "params", None)
        return {"Data": []}

    client._api = MagicMock()
    client._api.request.side_effect = _request

    with patch(
        "saxo_api_client.contrib.client.account_info",
        return_value=SimpleNamespace(ClientKey="ck-fetched", AccountKey="ak-fetched"),
    ):
        client.get_positions_query()

    assert captured["params"]["ClientKey"] == "ck-fetched"
    assert client.client_key == "ck-fetched"
    assert client.account_key == "ak-fetched"


def test_get_all_open_orders_fills_client_key_when_omitted() -> None:
    client = SaxoClient(access_token="dummy")
    client._client_key = "ck-orders"
    captured: dict = {}

    def _request(cmd: object) -> dict:
        captured["params"] = getattr(cmd, "params", None)
        return {"Data": []}

    client._api = MagicMock()
    client._api.request.side_effect = _request

    client.get_all_open_orders()

    assert captured["params"]["ClientKey"] == "ck-orders"


def test_explicit_client_key_wins() -> None:
    client = SaxoClient(access_token="dummy")
    client._client_key = "ck-default"
    captured: dict = {}

    def _request(cmd: object) -> dict:
        captured["params"] = getattr(cmd, "params", None)
        return {"Data": []}

    client._api = MagicMock()
    client._api.request.side_effect = _request

    client.get_positions_query(client_key="ck-explicit", account_key="ak-explicit")

    assert captured["params"]["ClientKey"] == "ck-explicit"
    assert captured["params"]["AccountKey"] == "ak-explicit"
