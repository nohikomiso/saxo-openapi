from typing import Any, Optional

import saxo_api_client.definitions.orders as OD
import saxo_api_client.endpoints.portfolio as pf
import saxo_api_client.endpoints.portfolio.clients as pfc
import saxo_api_client.endpoints.referencedata as rd
import saxo_api_client.endpoints.trading as tr
from saxo_api_client import API
from saxo_api_client.auth.client import SaxoAuthClient
from saxo_api_client.contrib.orders import (
    LimitOrder,
    MarketOrder,
    PositionClose,
    PositionOpen,
    StopIfTradedOrder,
    StopLimitOrder,
    StopOrder,
)
from saxo_api_client.contrib.orders.helper import tie_account_to_order
from saxo_api_client.contrib.session import account_info
from saxo_api_client.contrib.util.instrument_to_uic import InstrumentToUic
from saxo_api_client.exceptions import OpenAPIError


_OPTION_ASSET_TYPES: frozenset[str] = frozenset(
    {
        OD.AssetType.StockOption,
        OD.AssetType.StockIndexOption,
        OD.AssetType.FuturesOption,
        OD.AssetType.CfdIndexOption,
    }
)

_OPTION_ROUTE_MSG = (
    "AssetType={asset_type!r} requires OptionTrader with to_open_close="
    "'ToOpen'|'ToClose'. SaxoClient open_*/close_* paths do not support options "
    "(IsForceOpen / PositionOpen-Close are for FX/Stock/CFD)."
)


class SaxoClient:
    """
    High-level facade for Saxo Bank OpenAPI (Layer 3).

    Provides one-liner methods for balances, positions, market schedules, and
    orders while hiding endpoint Command classes. Prefer this for FX / Stock /
    CFD trading; use OptionTrader for options.
    """

    def __init__(
        self,
        auth_client: Optional[SaxoAuthClient] = None,
        access_token: Optional[str] = None,
        request_params: Optional[dict] = None,
    ):
        """Initialize with either auth_client or access_token."""
        self._api = API(access_token=access_token, auth_client=auth_client, request_params=request_params)
        self._account_key = None
        self._instrument_cache: dict[str, dict] = {}

    @property
    def account_key(self) -> str:
        """Get the default AccountKey, fetching it if necessary."""
        if self._account_key is None:
            self._account_key = account_info(self._api).AccountKey
        return self._account_key

    def _resolve_uic(self, Uic: Optional[int], Symbol: Optional[str], AssetType: str) -> int:
        """Resolve Uic from either explicit Uic or by querying the Symbol."""
        if Uic is not None:
            return Uic
        if Symbol is not None:
            spec = {"Instrument": Symbol}
            spec = InstrumentToUic(self._api, self.account_key, spec, assettype=AssetType)
            return spec["Uic"]
        raise ValueError("Either Uic or Symbol must be provided")

    @staticmethod
    def _reject_option_asset_type(asset_type: str) -> None:
        """Fail fast: options need OptionTrader + ToOpenClose, not PositionOpen/Close."""
        if asset_type in _OPTION_ASSET_TYPES:
            raise ValueError(_OPTION_ROUTE_MSG.format(asset_type=asset_type))

    def _execute_order(self, order_spec: dict | Any, validate_only: bool = False) -> dict:
        """Bind account and execute or precheck order."""
        order_spec_with_account = tie_account_to_order(self.account_key, order_spec)
        asset_type = order_spec_with_account.get("AssetType")

        if asset_type in [OD.AssetType.Stock, OD.AssetType.StockOption]:
            order_spec_with_account.pop("IsForceOpen", None)

        if validate_only:
            r = tr.orders.PrecheckOrder(data=order_spec_with_account)
        else:
            r = tr.orders.Order(data=order_spec_with_account)

        try:
            return self._api.request(r)
        except OpenAPIError as err:
            content = err.content or ""
            if "OrderRelatedPositionIsClosed" in content:
                hint = (
                    " Hint: PositionId is stale after a ForceOpen partial close; "
                    "re-query with resolve_force_open_close_target (or iter_open_positions) "
                    "and close the remaining RelatedPositionId / FO leg."
                )
                raise OpenAPIError(err.code, err.reason, content + hint) from err
            raise

    def place_order(self, order_data: dict | Any) -> dict:
        """Place an order from a builder instance or fully constructed dict."""
        return self._execute_order(order_data, validate_only=False)

    # ---------------------------------------------------------
    # Portfolio & Account (Read Operations)
    # ---------------------------------------------------------

    def get_client_details(self) -> dict:
        """Get client details including netting configuration."""
        r = pfc.ClientDetailsMe()
        return self._api.request(r)

    def summarize_client_netting(self) -> dict[str, Any]:
        """Summarize account netting / ForceOpen defaults for logging and preflight.

        Does **not** choose order routes. Explicit ``is_force_open`` / FO
        ``position_id`` / Option ``ToOpenClose`` remain the source of truth.
        Propagates API errors from :meth:`get_client_details`.
        """
        data = self.get_client_details()
        mode = data.get("PositionNettingMode")
        profile = data.get("PositionNettingProfile")
        method = data.get("PositionNettingMethod")
        force_default = data.get("ForceOpenDefaultValue")
        allowed = data.get("AllowedNettingProfiles")

        notes: list[str] = [
            "Order routes are chosen by position IsForceOpen / AssetType / intent — "
            "not by account netting settings alone. Do not auto-pick close_fifo vs "
            "close_force_open from this summary."
        ]
        mode_str = str(mode) if mode is not None else ""
        if mode_str == "EndOfDay" or "EndOfDay" in mode_str:
            notes.append(
                "PositionNettingMode is EndOfDay: closed legs may remain visible "
                "until EOD batch — do not treat residual visibility as open exposure "
                "or close again (zombie positions)."
            )
        if force_default is True:
            notes.append(
                "ForceOpenDefaultValue is True (GUI/omit defaults lean hedge). "
                "Always pass explicit is_force_open= on SaxoClient.open_* / builders."
            )

        return {
            "position_netting_mode": mode,
            "position_netting_profile": profile,
            "position_netting_method": method,
            "force_open_default_value": force_default,
            "allowed_netting_profiles": allowed,
            "notes": notes,
            "raw": data,
        }

    def get_accounts(self) -> dict:
        """Get a list of all accounts."""
        r = pf.accounts.AccountsMe()
        return self._api.request(r)

    def get_account_balance(self, client_key: Optional[str] = None) -> dict:
        """Get the current balance and margin details for the account."""
        kwargs = {"ClientKey": client_key} if client_key else {}
        r = pf.balances.AccountBalancesMe()
        if kwargs:
            r.params = kwargs
        return self._api.request(r)

    def get_positions(
        self,
        client_key: Optional[str] = None,
        field_groups: str = "PositionBase,PositionView,DisplayAndFormat,Greeks,UnderlyingDisplayAndFormat",
    ) -> dict:
        """Get all open net positions with rich default fields for options trading."""
        kwargs: dict[str, Any] = {"FieldGroups": field_groups}
        if client_key:
            kwargs["ClientKey"] = client_key
        r = pf.netpositions.NetPositionsMe(**kwargs)
        return self._api.request(r)

    def get_open_orders(self) -> dict:
        """Get open orders for the logged-in user."""
        r = pf.orders.GetOpenOrdersMe()
        return self._api.request(r)

    def get_active_orders(
        self,
        client_key: Optional[str] = None,
        status: str = "Working",
        field_groups: str = "DisplayAndFormat,ExchangeInfo",
    ) -> dict:
        """Get a list of active (working) orders with rich default fields."""
        kwargs: dict[str, Any] = {"Status": status, "FieldGroups": field_groups}
        if client_key:
            kwargs["ClientKey"] = client_key
        r = pf.orders.OrdersMe(**kwargs)
        return self._api.request(r)

    def get_positions_query(
        self,
        client_key: Optional[str] = None,
        account_key: Optional[str] = None,
        field_groups: str = "PositionBase,PositionView,DisplayAndFormat,Greeks,UnderlyingDisplayAndFormat",
    ) -> dict:
        """Query individual positions (not net positions) with rich fields."""
        kwargs: dict[str, Any] = {"FieldGroups": field_groups}
        if client_key:
            kwargs["ClientKey"] = client_key
        if account_key:
            kwargs["AccountKey"] = account_key
        r = pf.positions.PositionsQuery(params=kwargs)
        return self._api.request(r)

    def get_all_open_orders(
        self,
        client_key: Optional[str] = None,
        account_key: Optional[str] = None,
        field_groups: str = "DisplayAndFormat,ExchangeInfo",
    ) -> dict:
        """Query all open orders across the account."""
        kwargs: dict[str, Any] = {"FieldGroups": field_groups}
        if client_key:
            kwargs["ClientKey"] = client_key
        if account_key:
            kwargs["AccountKey"] = account_key
        r = pf.orders.GetAllOpenOrders(params=kwargs)
        return self._api.request(r)

    # ---------------------------------------------------------
    # Market Data & Schedule
    # ---------------------------------------------------------

    def get_instrument_details(
        self,
        asset_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
    ) -> dict:
        """Fetch detailed specifications (lot size, tick size, etc) for an instrument."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)

        cache_key = f"{uic_resolved}_{asset_type}"
        if cache_key in self._instrument_cache:
            return self._instrument_cache[cache_key]

        params = {"AccountKey": self.account_key}
        r = rd.instruments.InstrumentDetails(Uic=uic_resolved, AssetType=asset_type, params=params)
        rv = self._api.request(r)
        self._instrument_cache[cache_key] = rv
        return rv

    def get_market_schedule(
        self,
        asset_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
    ) -> dict:
        """Fetch trading sessions/schedule for the instrument."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        r = rd.instruments.TradingSchedule(Uic=uic_resolved, AssetType=asset_type)
        return self._api.request(r)

    def get_current_session_state(
        self,
        asset_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
    ) -> Optional[str]:
        """Return current session state (e.g. AutomatedTrading, Closed)."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        schedule = self.get_market_schedule(asset_type=asset_type, uic=uic_resolved)
        sessions = schedule.get("Sessions", [])
        if not sessions:
            return "Closed"
        return sessions[0].get("State", "Closed")

    def is_order_accepted(
        self,
        asset_type: str,
        order_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
    ) -> bool:
        """True when the instrument session is AutomatedTrading."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        state = self.get_current_session_state(asset_type=asset_type, uic=uic_resolved)
        return state == "AutomatedTrading"

    def get_prices(
        self,
        asset_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
    ) -> dict:
        """Get current Ask/Bid prices for the instrument."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        r = tr.infoprices.InfoPrice(params={"Uic": uic_resolved, "AssetType": asset_type})
        return self._api.request(r)

    def get_price_quotes(self, uics: list[int], asset_type: str = "Stock") -> dict:
        """Get snapshot of current prices (Quote field group)."""
        uic_str = ",".join(map(str, uics))
        params = {"Uics": uic_str, "FieldGroups": "Quote", "AssetType": asset_type}
        r = tr.infoprices.InfoPrices(params=params)
        return self._api.request(r)

    # ---------------------------------------------------------
    # Order Execution (Write Operations)
    # ---------------------------------------------------------

    def market_order(
        self,
        asset_type: str,
        amount: int | float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Place a Market Order."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = MarketOrder(Uic=uic_resolved, Amount=amount, AssetType=asset_type, **kwargs)
        return self._execute_order(order)

    def limit_order(
        self,
        asset_type: str,
        amount: int | float,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Place a Limit Order."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = LimitOrder(
            Uic=uic_resolved,
            Amount=amount,
            OrderPrice=order_price,
            AssetType=asset_type,
            **kwargs,
        )
        return self._execute_order(order)

    def stop_order(
        self,
        asset_type: str,
        amount: int | float,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Place a Stop Order with smart routing (Stop vs StopIfTraded)."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        details = self.get_instrument_details(asset_type=asset_type, uic=uic_resolved)
        supported_types = details.get("SupportedOrderTypes", [])

        if "Stop" in supported_types:
            order = StopOrder(Uic=uic_resolved, Amount=amount, OrderPrice=order_price, AssetType=asset_type, **kwargs)
        elif "StopIfTraded" in supported_types:
            order = StopIfTradedOrder(
                Uic=uic_resolved,
                Amount=amount,
                OrderPrice=order_price,
                AssetType=asset_type,
                **kwargs,
            )
        else:
            order = StopOrder(Uic=uic_resolved, Amount=amount, OrderPrice=order_price, AssetType=asset_type, **kwargs)

        return self._execute_order(order)

    def stop_limit_order(
        self,
        asset_type: str,
        amount: int | float,
        order_price: float,
        stop_limit_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Place a Stop Limit Order."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = StopLimitOrder(
            Uic=uic_resolved,
            Amount=amount,
            OrderPrice=order_price,
            StopLimitPrice=stop_limit_price,
            AssetType=asset_type,
            **kwargs,
        )
        return self._execute_order(order)

    def stop_if_traded_order(
        self,
        asset_type: str,
        amount: int | float,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Place an explicit StopIfTraded Order."""
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = StopIfTradedOrder(
            Uic=uic_resolved,
            Amount=amount,
            OrderPrice=order_price,
            AssetType=asset_type,
            **kwargs,
        )
        return self._execute_order(order)

    def validate_order(self, order_spec: dict[str, Any] | Any) -> dict:
        """Precheck an order without placing it (PrecheckOrder endpoint)."""
        return self._execute_order(order_spec, validate_only=True)

    def cancel_order(self, order_id: str) -> dict:
        """Cancel an active order by ID."""
        r = tr.orders.CancelOrders(OrderIds=str(order_id), params={"AccountKey": self.account_key})
        return self._api.request(r)

    # ---------------------------------------------------------
    # Position open / close (intent-named; prefer over market_order for FO)
    # ---------------------------------------------------------

    def iter_open_positions(
        self,
        *,
        uic: Optional[int] = None,
        asset_type: Optional[str] = None,
        client_key: Optional[str] = None,
        account_key: Optional[str] = None,
        field_groups: str = "PositionBase,PositionView,DisplayAndFormat",
    ) -> list[dict[str, Any]]:
        """Return normalized open legs from PositionsQuery.

        ``position_id`` is taken from the top-level PositionsQuery item (not
        only PositionBase), matching Saxo SIM responses.
        """
        body = self.get_positions_query(
            client_key=client_key,
            account_key=account_key or self.account_key,
            field_groups=field_groups,
        )
        rows: list[dict[str, Any]] = []
        for item in body.get("Data") or []:
            base = item.get("PositionBase") or {}
            view = item.get("PositionView") or {}
            item_uic = base.get("Uic")
            item_asset = base.get("AssetType")
            if uic is not None and int(item_uic or -1) != int(uic):
                continue
            if asset_type is not None and item_asset != asset_type:
                continue
            position_id = item.get("PositionId") or base.get("PositionId")
            amount = float(base.get("Amount") or 0)
            rows.append(
                {
                    "position_id": str(position_id) if position_id is not None else None,
                    "uic": int(item_uic) if item_uic is not None else None,
                    "asset_type": item_asset,
                    "amount": amount,
                    "buy_sell": OD.Direction.Buy if amount > 0 else OD.Direction.Sell,
                    "is_force_open": bool(base.get("IsForceOpen")),
                    "open_price": base.get("OpenPrice"),
                    "status": base.get("Status"),
                    "related_position_id": (
                        str(base["RelatedPositionId"]) if base.get("RelatedPositionId") is not None else None
                    ),
                    "can_be_closed": base.get("CanBeClosed"),
                    "external_reference": base.get("ExternalReference"),
                    "profit_loss": view.get("ProfitLossOnTrade"),
                    "current_price": view.get("CurrentPrice"),
                    "raw": item,
                }
            )
        return rows

    def _require_force_open_position(self, position_id: str) -> dict[str, Any]:
        for row in self.iter_open_positions():
            if row.get("position_id") == str(position_id):
                if not row.get("is_force_open"):
                    raise ValueError(
                        f"position_id={position_id} is not ForceOpen; "
                        "use close_fifo_* for FIFO/netting closes"
                    )
                return row
        raise ValueError(f"position_id={position_id} not found among open positions")

    def resolve_force_open_close_target(
        self,
        *,
        previous_position_id: str,
        uic: int,
        asset_type: Optional[str] = None,
        preferred_buy_sell: Optional[str] = None,
        client_key: Optional[str] = None,
        account_key: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Re-resolve the remaining ForceOpen leg after a partial close.

        Saxo may retire the original ``PositionId`` (PartiallyClosed) and expose
        the remainder via ``RelatedPositionId`` or a new FO row for the same UIC.
        Returns a normalized ``iter_open_positions`` row, or ``None`` if nothing
        remains to close (skip remainder close).
        """
        prev = str(previous_position_id)
        rows = self.iter_open_positions(
            uic=uic,
            asset_type=asset_type,
            client_key=client_key,
            account_key=account_key,
        )
        by_id = {str(r["position_id"]): r for r in rows if r.get("position_id")}

        def _open_amount(row: dict[str, Any]) -> float:
            return abs(float(row.get("amount") or 0))

        # 1) Same id still has residual size
        if prev in by_id and _open_amount(by_id[prev]) > 1e-9:
            return by_id[prev]

        # 2) Follow RelatedPositionId from the previous row (if still listed)
        if prev in by_id:
            related = by_id[prev].get("related_position_id")
            if related and str(related) in by_id and _open_amount(by_id[str(related)]) > 1e-9:
                return by_id[str(related)]

        # 3) Rows that list prev as RelatedPositionId (remainder child)
        related_children = [
            r
            for r in rows
            if r.get("related_position_id") == prev and _open_amount(r) > 1e-9 and r.get("is_force_open")
        ]
        if related_children:
            related_children.sort(key=_open_amount, reverse=True)
            return related_children[0]

        # 4) Fallback: remaining FO legs on UIC (optionally same side)
        candidates: list[dict[str, Any]] = []
        for r in rows:
            if str(r.get("position_id")) == prev:
                continue
            if not r.get("is_force_open") or _open_amount(r) <= 1e-9:
                continue
            if preferred_buy_sell and r.get("buy_sell") != preferred_buy_sell:
                continue
            candidates.append(r)
        if not candidates:
            return None
        candidates.sort(key=_open_amount, reverse=True)
        return candidates[0]

    def reduce_force_open_leg(
        self,
        *,
        position_id: str,
        asset_type: str,
        uic: int,
        amount: int | float,
        buy_sell: str,
        close_remainder: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Partial FO close then optionally close the re-resolved remainder.

        After the partial, uses :meth:`resolve_force_open_close_target`. If the
        target is gone, remainder close is skipped (no stale PositionId error).
        """
        self._reject_option_asset_type(asset_type)
        partial = self.close_force_open_market(
            position_id=position_id,
            asset_type=asset_type,
            uic=uic,
            amount=amount,
            buy_sell=buy_sell,
            **kwargs,
        )
        out: dict[str, Any] = {"partial": partial, "remainder": None, "skipped_remainder": False}
        if not close_remainder:
            return out
        # Remaining leg keeps the original position side (opposite of the close order).
        position_side = "Buy" if buy_sell == "Sell" else "Sell"
        target = self.resolve_force_open_close_target(
            previous_position_id=position_id,
            uic=uic,
            asset_type=asset_type,
            preferred_buy_sell=position_side,
        )
        if target is None or abs(float(target.get("amount") or 0)) <= 1e-9:
            out["skipped_remainder"] = True
            return out
        rem_amt = abs(float(target["amount"]))
        rem_side = "Sell" if float(target.get("amount") or 0) > 0 else "Buy"
        out["remainder"] = self.close_force_open_market(
            position_id=str(target["position_id"]),
            asset_type=asset_type,
            uic=uic,
            amount=rem_amt,
            buy_sell=rem_side,
            **kwargs,
        )
        return out

    def open_market(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        is_force_open: bool,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Open a new position (market). ``is_force_open`` is required.

        Not for StockOption / index options — use ``OptionTrader`` with ``to_open_close``.
        """
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionOpen.market(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            is_force_open=is_force_open,
            **kwargs,
        )
        return self._execute_order(order)

    def open_limit(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        is_force_open: bool,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Open a new position (limit). Not for options — use OptionTrader."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionOpen.limit(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            is_force_open=is_force_open,
            **kwargs,
        )
        return self._execute_order(order)

    def open_stop(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        is_force_open: bool,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Open a new position (stop). Not a close. Not for options — use OptionTrader."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionOpen.stop(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            is_force_open=is_force_open,
            **kwargs,
        )
        return self._execute_order(order)

    def open_stop_limit(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        stop_limit_price: float,
        is_force_open: bool,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """Open a new position (stop-limit). Not for options — use OptionTrader."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionOpen.stop_limit(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            stop_limit_price=stop_limit_price,
            is_force_open=is_force_open,
            **kwargs,
        )
        return self._execute_order(order)

    def close_fifo_market(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """FIFO/netting close via opposite market (no PositionId). Not for options."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.fifo_market(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            **kwargs,
        )
        return self._execute_order(order)

    def close_fifo_limit(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """FIFO/netting close via opposite limit. Not for options."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.fifo_limit(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order)

    def close_fifo_stop(
        self,
        *,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        **kwargs: Any,
    ) -> dict:
        """FIFO/netting close via opposite stop. Not for options."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.fifo_stop(
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order)

    def close_force_open_market(
        self,
        *,
        position_id: str,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        verify_position: bool = True,
        **kwargs: Any,
    ) -> dict:
        """ForceOpen explicit market close (PositionId + nested Orders). Not for options."""
        self._reject_option_asset_type(asset_type)
        if verify_position:
            self._require_force_open_position(position_id)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.force_open_market(
            position_id=position_id,
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            **kwargs,
        )
        return self._execute_order(order)

    def close_force_open_limit(
        self,
        *,
        position_id: str,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        verify_position: bool = True,
        **kwargs: Any,
    ) -> dict:
        """ForceOpen explicit limit close. Not for options."""
        self._reject_option_asset_type(asset_type)
        if verify_position:
            self._require_force_open_position(position_id)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.force_open_limit(
            position_id=position_id,
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order)

    def close_force_open_stop(
        self,
        *,
        position_id: str,
        asset_type: str,
        amount: int | float,
        buy_sell: str,
        order_price: float,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        verify_position: bool = True,
        **kwargs: Any,
    ) -> dict:
        """ForceOpen explicit stop close (requires correct market side). Not for options."""
        self._reject_option_asset_type(asset_type)
        if verify_position:
            self._require_force_open_position(position_id)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        order = PositionClose.force_open_stop(
            position_id=position_id,
            uic=uic_resolved,
            amount=amount,
            asset_type=asset_type,
            buy_sell=buy_sell,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order)

    def flatten_force_open(
        self,
        *,
        asset_type: str,
        symbol: Optional[str] = None,
        uic: Optional[int] = None,
        external_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """Flatten net exposure for a UIC with ClearForceOpen market. Not for options."""
        self._reject_option_asset_type(asset_type)
        uic_resolved = self._resolve_uic(uic, symbol, asset_type)
        net = 0.0
        for row in self.iter_open_positions(uic=uic_resolved, asset_type=asset_type):
            net += float(row.get("amount") or 0)
        if abs(net) < 1e-9:
            return {"ok": True, "skipped": True, "net": 0.0}
        flatten_amt = -net
        buy_sell = OD.Direction.Buy if flatten_amt > 0 else OD.Direction.Sell
        order = PositionClose.clear_force_open_market(
            uic=uic_resolved,
            amount=abs(flatten_amt),
            asset_type=asset_type,
            buy_sell=buy_sell,
            external_reference=external_reference,
        )
        resp = self._execute_order(order)
        return {
            "ok": True,
            "skipped": False,
            "net_before": net,
            "buy_sell": buy_sell,
            "order_id": str(resp.get("OrderId") or ""),
            "raw": resp,
        }

    # ---------------------------------------------------------
    # Streaming & Subscriptions
    # ---------------------------------------------------------

    def add_price_subscription(
        self,
        context_id: str,
        reference_id: str,
        uic: int,
        asset_type: str,
        arguments: Optional[dict] = None,
    ) -> dict:
        """Create a new price subscription."""
        if arguments is None:
            arguments = {"Uic": uic, "AssetType": asset_type}

        data = {
            "ContextId": context_id,
            "ReferenceId": reference_id,
            "Arguments": arguments,
        }
        r = tr.prices.CreatePriceSubscription(data=data)
        return self._api.request(r)

    def remove_price_subscription(self, context_id: str, reference_id: str) -> dict:
        """Remove a specific price subscription."""
        r = tr.prices.PriceSubscriptionRemove(ContextId=context_id, ReferenceId=reference_id)
        return self._api.request(r)

    def remove_all_subscriptions(self, context_id: str) -> dict:
        """Remove all active subscriptions for a context."""
        from saxo_api_client.endpoints.rootservices.subscriptions import RemoveMultipleActiveSubscriptions

        r = RemoveMultipleActiveSubscriptions(ContextId=context_id, params={})
        return self._api.request(r)
