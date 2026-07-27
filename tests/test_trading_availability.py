"""TradingSchedule 404 fallback for get_trading_availability."""

from __future__ import annotations

from unittest.mock import MagicMock

from saxo_api_client.contrib.client import SaxoClient
from saxo_api_client.exceptions import OpenAPIError


def test_trading_availability_falls_back_on_schedule_404() -> None:
    client = SaxoClient(access_token="dummy")
    client._account_key = "ak"
    client._client_key = "ck"
    client._api = MagicMock()

    def _schedule(*_a: object, **_k: object) -> dict:
        raise OpenAPIError(404, "Not Found", None)

    client.get_market_schedule = _schedule  # type: ignore[method-assign]
    client.get_price_quotes = MagicMock(  # type: ignore[method-assign]
        return_value={
            "Data": [
                {
                    "Quote": {
                        "MarketState": "Open",
                        "Bid": 1.0,
                        "Ask": 1.1,
                    }
                }
            ]
        }
    )
    client.get_instrument_details = MagicMock(  # type: ignore[method-assign]
        return_value={"TradingStatus": "Tradable", "IsTradable": True}
    )

    avail = client.get_trading_availability(asset_type="CfdOnIndex", uic=4913)
    assert avail["tradable_now"] is True
    assert avail["schedule_source"] == "fallback_quote"
    assert avail["schedule_error"]
    assert avail["quote_state"] == "Open"


def test_trading_availability_uses_schedule_when_present() -> None:
    client = SaxoClient(access_token="dummy")
    client._account_key = "ak"
    client.get_market_schedule = MagicMock(  # type: ignore[method-assign]
        return_value={
            "Sessions": [
                {
                    "StartTime": "2000-01-01T00:00:00.000000Z",
                    "EndTime": "2099-01-01T00:00:00.000000Z",
                    "State": "AutomatedTrading",
                }
            ]
        }
    )
    client.get_price_quotes = MagicMock(return_value={"Data": [{}]})  # type: ignore[method-assign]
    client.get_instrument_details = MagicMock(return_value={})  # type: ignore[method-assign]

    avail = client.get_trading_availability(asset_type="CfdOnStock", uic=30424)
    assert avail["tradable_now"] is True
    assert avail["schedule_source"] == "TradingSchedule"
    assert avail["schedule_current"]["state"] == "AutomatedTrading"
