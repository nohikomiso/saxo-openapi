from typing import Any

import saxo_openapi.definitions.orders as OD
import saxo_openapi.endpoints.referencedata as rd
import saxo_openapi.endpoints.trading as tr
from saxo_openapi import API
from saxo_openapi.contrib.orders import (
    LimitOrder,
    MarketOrder,
    StopIfTradedOrder,
    StopLimitOrder,
    StopOrder,
    tie_account_to_order,
)
from saxo_openapi.contrib.session import account_info


class SaxoTrader:
    """
    SaxoTrader is a high-level helper class to simplify order placement.
    It manages the AccountKey automatically and provides simple methods
    for common trading operations, including smart order routing.
    """

    def __init__(self, client: API, account_key: str | None = None):
        """
        Initialize SaxoTrader.

        :param client: An initialized API client instance.
        :param account_key: Optional AccountKey. If not provided, it will be fetched automatically on first use.
        """
        self.client = client
        self._account_key = account_key
        self._instrument_cache: dict[str, dict] = {}

    @property
    def account_key(self) -> str:
        """Get the AccountKey, fetching it if necessary."""
        if self._account_key is None:
            self._account_key = account_info(self.client).AccountKey
        return self._account_key

    def _execute_order(self, order_spec: dict | Any, validate_only: bool = False) -> dict:
        """
        Internal helper to bind account and execute order.

        :param order_spec: Order specification (dict or Helper class)
        :param validate_only: If True, only performs pre-check without placing order.
        """
        order_spec_with_account = tie_account_to_order(self.account_key, order_spec)

        # Stock/StockOption/etc do not support IsForceOpen.
        # Check AssetType to clean up parameters safely.
        asset_type = order_spec_with_account.get("AssetType")
        if asset_type in [OD.AssetType.Stock, OD.AssetType.StockOption]:
            # Clean up unsupported fields for Stock family
            order_spec_with_account.pop("IsForceOpen", None)

        if validate_only:
            # Use PrecheckOrder endpoint
            r = tr.orders.PrecheckOrder(data=order_spec_with_account)
        else:
            # Place actual Order
            r = tr.orders.Order(data=order_spec_with_account)

        return self.client.request(r)

    def _get_instrument_details(self, Uic: int, AssetType: str) -> dict:
        """Fetch and cache instrument details."""
        cache_key = f"{Uic}_{AssetType}"
        if cache_key in self._instrument_cache:
            return self._instrument_cache[cache_key]

        params = {"AccountKey": self.account_key}
        r = rd.instruments.InstrumentDetails(Uic=Uic, AssetType=AssetType, params=params)
        rv = self.client.request(r)
        self._instrument_cache[cache_key] = rv
        return rv

    def validate_order(self, order_spec: dict | Any) -> dict:
        """
        Validate an order specification using Saxo's PrecheckOrder endpoint.
        Useful for checking parameters, price distance (WrongSideOfMarket), etc.
        without actually placing the order.
        """
        return self._execute_order(order_spec, validate_only=True)

    def market_order(
        self,
        Uic: int,
        Amount: int | float,
        AssetType: str = OD.AssetType.FxSpot,
        **kwargs,
    ) -> dict:
        """Place a Market Order."""
        order = MarketOrder(Uic=Uic, Amount=Amount, AssetType=AssetType, **kwargs)
        return self._execute_order(order)

    def limit_order(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: float,
        AssetType: str = OD.AssetType.FxSpot,
        **kwargs,
    ) -> dict:
        """Place a Limit Order."""
        order = LimitOrder(Uic=Uic, Amount=Amount, OrderPrice=OrderPrice, AssetType=AssetType, **kwargs)
        return self._execute_order(order)

    def stop_order(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: float,
        AssetType: str = OD.AssetType.FxSpot,
        **kwargs,
    ) -> dict:
        """
        Place a Stop Order with Smart Routing.
        Automatically checks SupportedOrderTypes for the instrument.
        """
        details = self._get_instrument_details(Uic, AssetType)
        supported_types = details.get("SupportedOrderTypes", [])

        if "Stop" in supported_types:
            order = StopOrder(
                Uic=Uic,
                Amount=Amount,
                OrderPrice=OrderPrice,
                AssetType=AssetType,
                **kwargs,
            )
        elif "StopIfTraded" in supported_types:
            order = StopIfTradedOrder(
                Uic=Uic,
                Amount=Amount,
                OrderPrice=OrderPrice,
                AssetType=AssetType,
                **kwargs,
            )
        else:
            # Fallback
            order = StopOrder(
                Uic=Uic,
                Amount=Amount,
                OrderPrice=OrderPrice,
                AssetType=AssetType,
                **kwargs,
            )

        return self._execute_order(order)

    def stop_limit_order(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: float,
        StopLimitPrice: float,
        AssetType: str = OD.AssetType.FxSpot,
        **kwargs,
    ) -> dict:
        """Place a Stop Limit Order."""
        order = StopLimitOrder(
            Uic=Uic,
            Amount=Amount,
            OrderPrice=OrderPrice,
            StopLimitPrice=StopLimitPrice,
            AssetType=AssetType,
            **kwargs,
        )
        return self._execute_order(order)

    def stop_if_traded_order(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: float,
        AssetType: str = OD.AssetType.FxSpot,
        **kwargs,
    ) -> dict:
        """Place a Stop If Traded Order explicitly."""
        order = StopIfTradedOrder(Uic=Uic, Amount=Amount, OrderPrice=OrderPrice, AssetType=AssetType, **kwargs)
        return self._execute_order(order)
