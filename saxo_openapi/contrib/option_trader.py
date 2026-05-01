"""Option trader helper for placing option orders."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import saxo_openapi.definitions.orders as OD
import saxo_openapi.endpoints.trading as tr
import saxo_openapi.endpoints.trading.multilegorders as mo
from saxo_openapi.contrib.option_finder import OptionFinder
from saxo_openapi.contrib.orders import tie_account_to_order
from saxo_openapi.contrib.session import account_info

if TYPE_CHECKING:
    from saxo_openapi import API


class OptionTrader:
    """オプション取引に特化した高レベルヘルパークラス

    オプション契約の検索から注文発注までを簡素化するメソッドを提供します。

    使用例:
    ```python
    trader = OptionTrader(client)

    # 方法1: Uicで直接注文
    order = trader.buy_option(uic=12345, amount=1, order_price=3.50)

    # 方法2: キーワードから注文（内部で検索）
    order = trader.buy_call(
        keyword="AMD",
        expiry_date="2026-02-06",
        strike_price=240.0,
        amount=1,
        order_price=3.50
    )
    ```
    """

    def __init__(self, client: API, account_key: str | None = None):
        """
        OptionTrader を初期化

        :param client: APIクライアント
        :param account_key: アカウントキー（Noneの場合は自動取得）
        """
        self.client = client
        self._account_key = account_key
        self.finder = OptionFinder(client, account_key)

    @property
    def account_key(self) -> str:
        """AccountKey を取得"""
        if self._account_key is None:
            self._account_key = account_info(self.client).AccountKey
        return self._account_key

    def _build_option_order(
        self,
        uic: int,
        amount: int,
        buy_sell: str,
        order_type: str,
        asset_type: str,
        to_open_close: str,
        order_price: float | None = None,
        order_duration: dict[str, Any] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """オプション注文の辞書を構築"""
        order_spec: dict[str, Any] = {
            "Uic": uic,
            "AssetType": asset_type,
            "Amount": abs(amount),
            "BuySell": buy_sell,
            "OrderType": order_type,
            "ToOpenClose": to_open_close,
            "ManualOrder": False,
        }

        # 指値価格（Limit/StopLimit注文の場合）
        if order_type in ["Limit", "StopLimit"] and order_price is not None:
            order_spec["OrderPrice"] = order_price

        # 注文期間（デフォルト: DayOrder）
        if order_duration:
            order_spec["OrderDuration"] = order_duration
        else:
            order_spec["OrderDuration"] = {"DurationType": OD.OrderDurationType.DayOrder}

        # 追加オプション
        order_spec.update(kwargs)

        return order_spec

    def _execute_order(self, order_spec: dict[str, Any], validate_only: bool = False) -> dict[str, Any]:
        """注文を実行する内部ヘルパー"""
        order_spec_with_account = tie_account_to_order(self.account_key, order_spec)

        r: Any
        if validate_only:
            r = tr.orders.PrecheckOrder(data=order_spec_with_account)
        else:
            r = tr.orders.Order(data=order_spec_with_account)

        result = self.client.request(r)
        return result if isinstance(result, dict) else {}

    # ========== Uic直接指定（効率的） ==========

    def buy_option(
        self,
        uic: int,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプション買い注文

        :param uic: オプション契約のUic（ContractOptionSpacesで取得）
        :param amount: 契約数（正の値）
        :param to_open_close: "ToOpen" or "ToClose" （必須）
        :param order_type: 注文タイプ（"Market" or "Limit"）
        :param order_price: 指値価格（Limitの場合必須）
        :param asset_type: 資産タイプ
        :return: 注文レスポンス
        """
        if order_type == "Limit" and order_price is None:
            raise ValueError("order_price is required for Limit orders")

        order_spec = self._build_option_order(
            uic=uic,
            amount=amount,
            buy_sell=OD.Direction.Buy,
            order_type=order_type,
            asset_type=asset_type,
            to_open_close=to_open_close,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order_spec)

    def sell_option(
        self,
        uic: int,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプション売り注文

        :param uic: オプション契約のUic
        :param amount: 契約数（正の値）
        :param to_open_close: "ToOpen"（新規売建）or "ToClose"（決済）（必須）
        :param order_type: 注文タイプ
        :param order_price: 指値価格（Limitの場合必須）
        :param asset_type: 資産タイプ
        :return: 注文レスポンス
        """
        if order_type == "Limit" and order_price is None:
            raise ValueError("order_price is required for Limit orders")

        order_spec = self._build_option_order(
            uic=uic,
            amount=amount,
            buy_sell=OD.Direction.Sell,
            order_type=order_type,
            asset_type=asset_type,
            to_open_close=to_open_close,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order_spec)

    # ========== キーワード指定（便利メソッド） ==========

    def buy_call(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワードからコールオプション買い

        :param keyword: 検索キーワード（例: "AMD"）
        :param expiry_date: 満期日（YYYY-MM-DD形式）
        :param strike_price: 行使価格
        :param amount: 契約数
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :return: 注文レスポンス
        :raises ValueError: オプションが見つからない場合
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Call", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Call")
        return self.buy_option(
            uic=option.uic,
            amount=amount,
            to_open_close=to_open_close,
            order_type=order_type,
            order_price=order_price,
            asset_type=asset_type,
            **kwargs,
        )

    def buy_put(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワードからプットオプション買い

        :param keyword: 検索キーワード（例: "AMD"）
        :param expiry_date: 満期日（YYYY-MM-DD形式）
        :param strike_price: 行使価格
        :param amount: 契約数
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :return: 注文レスポンス
        :raises ValueError: オプションが見つからない場合
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Put", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Put")
        return self.buy_option(
            uic=option.uic,
            amount=amount,
            to_open_close=to_open_close,
            order_type=order_type,
            order_price=order_price,
            asset_type=asset_type,
            **kwargs,
        )

    def sell_call(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワードからコールオプション売り

        :param keyword: 検索キーワード（例: "AMD"）
        :param expiry_date: 満期日（YYYY-MM-DD形式）
        :param strike_price: 行使価格
        :param amount: 契約数
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :return: 注文レスポンス
        :raises ValueError: オプションが見つからない場合
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Call", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Call")
        return self.sell_option(
            uic=option.uic,
            amount=amount,
            to_open_close=to_open_close,
            order_type=order_type,
            order_price=order_price,
            asset_type=asset_type,
            **kwargs,
        )

    def sell_put(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワードからプットオプション売り

        :param keyword: 検索キーワード（例: "AMD"）
        :param expiry_date: 満期日（YYYY-MM-DD形式）
        :param strike_price: 行使価格
        :param amount: 契約数
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :return: 注文レスポンス
        :raises ValueError: オプションが見つからない場合
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Put", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Put")
        return self.sell_option(
            uic=option.uic,
            amount=amount,
            to_open_close=to_open_close,
            order_type=order_type,
            order_price=order_price,
            asset_type=asset_type,
            **kwargs,
        )

    # ========== ポジション管理 ==========

    def exercise_option(self, position_id: str, amount: int | None = None) -> dict:
        """
        オプション権利行使

        :param position_id: ポジションID
        :param amount: 行使数量（Noneの場合は全量）
        :return: 行使レスポンス
        """
        data: dict[str, Any] = {}
        if amount is not None:
            data["Amount"] = amount

        r = tr.positions.ExercisePosition(PositionId=position_id, data=data)
        return self.client.request(r)

    def close_option_position(
        self,
        uic: int,
        amount: int,
        order_type: str = "Market",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプションポジションをクローズ（反対売買）

        ロングポジションの場合は売り、ショートポジションの場合は買いを発注。
        amount の符号で方向を判定。

        :param uic: オプション契約のUic
        :param amount: 数量（正=買い決済、負=売り決済）
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :return: 注文レスポンス
        """
        if amount > 0:
            return self.buy_option(
                uic=uic,
                amount=amount,
                order_type=order_type,
                order_price=order_price,
                asset_type=asset_type,
                to_open_close="ToClose",
                **kwargs,
            )
        else:
            return self.sell_option(
                uic=uic,
                amount=abs(amount),
                order_type=order_type,
                order_price=order_price,
                asset_type=asset_type,
                to_open_close="ToClose",
                **kwargs,
            )

    # ========== 事前チェック ==========

    def validate_order(
        self,
        uic: int,
        amount: int,
        to_open_close: str,
        buy_sell: str = "Buy",
        order_type: str = "Limit",
        order_price: float | None = None,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプション注文を事前チェック（発注はしない）

        :param uic: オプション契約のUic
        :param amount: 契約数
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param buy_sell: "Buy" or "Sell"
        :param order_type: 注文タイプ
        :param order_price: 指値価格
        :param asset_type: 資産タイプ
        :return: 事前チェック結果
        """
        if order_type == "Limit" and order_price is None:
            raise ValueError("order_price is required for Limit orders")

        order_spec = self._build_option_order(
            uic=uic,
            amount=amount,
            buy_sell=buy_sell,
            order_type=order_type,
            asset_type=asset_type,
            to_open_close=to_open_close,
            order_price=order_price,
            **kwargs,
        )
        return self._execute_order(order_spec, validate_only=True)

    # ========== オプション戦略注文 (MultiLeg) ==========

    def get_strategy_defaults(
        self,
        option_root_id: int,
        strategy_type: str,  # OptionsStrategyType class constants
    ) -> dict[str, Any]:
        """
        オプション戦略の推奨レグ構成を取得

        :param option_root_id: オプションルートID
        :param strategy_type: 戦略タイプ (OptionsStrategyType.STRADDLE 等を使用)
        :return: 戦略デフォルト情報 (Legsなど)
        """
        params = {
            "OptionRootId": option_root_id,
            "OptionsStrategyType": strategy_type,
            "AccountKey": self.account_key,
        }
        r = mo.MultilegOrderDefaults(params=params)
        return self.client.request(r)

    def place_strategy_order(
        self,
        legs: list[dict[str, Any]],
        order_type: str = "Limit",
        order_price: float | None = None,
        order_duration: dict[str, Any] | None = None,
        manual_order: bool = False,
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプション戦略注文（マルチレッグ注文）を発注

        このメソッドは、全レグが「同時かつ対称的（Atomic）」に約定することを保証します。

        :param legs: 注文レグのリスト。get_strategy_defaultsの結果や手動構築した辞書リスト。
                     各レグは {Uic, AssetType, BuySell, Amount, ToOpenClose} などを含む。
        :param order_type: 注文タイプ ("Limit", "Market" 等)
        :param order_price: 注文価格 (全体のネット価格)。Limitの場合は必須。
        :param order_duration: 有効期限設定。Noneの場合はDayOrder。
        :param manual_order: 手動注文フラグ
        :return: 注文レスポンス (OrderId等)
        """
        if order_type == "Limit" and order_price is None:
            raise ValueError("order_price is required for Limit strategy orders")

        order_spec: dict[str, Any] = {
            "AccountKey": self.account_key,
            "Legs": legs,
            "OrderType": order_type,
            "ManualOrder": manual_order,
        }

        if order_price is not None:
            order_spec["OrderPrice"] = order_price

        if order_duration:
            order_spec["OrderDuration"] = order_duration
        else:
            order_spec["OrderDuration"] = {"DurationType": OD.OrderDurationType.DayOrder}

        order_spec.update(kwargs)

        r = mo.MultilegOrder(data=order_spec)
        return self.client.request(r)

    def precheck_strategy_order(
        self,
        legs: list[dict[str, Any]],
        order_type: str = "Limit",
        order_price: float | None = None,
        order_duration: dict[str, Any] | None = None,
        field_groups: list[str] | None = None,
        manual_order: bool = False,
        **kwargs,
    ) -> dict[str, Any]:
        """
        オプション戦略注文の事前チェック

        :param legs: 注文レグのリスト
        :param order_type: 注文タイプ
        :param order_price: 注文価格
        :param order_duration: 有効期限設定
        :param field_groups: 結果に含めるフィールド ("Costs", "MarginImpactBuySell" 等)
        :param manual_order: 手動注文フラグ
        :return: 事前チェック結果
        """
        order_spec: dict[str, Any] = {
            "AccountKey": self.account_key,
            "Legs": legs,
            "OrderType": order_type,
            "ManualOrder": manual_order,
        }

        if order_price is not None:
            order_spec["OrderPrice"] = order_price

        if order_duration:
            order_spec["OrderDuration"] = order_duration
        else:
            order_spec["OrderDuration"] = {"DurationType": OD.OrderDurationType.DayOrder}

        if field_groups:
            order_spec["FieldGroups"] = field_groups

        order_spec.update(kwargs)

        r = mo.MultilegOrderPrecheck(data=order_spec)
        return self.client.request(r)

    def cancel_strategy_order(self, multileg_order_id: str) -> dict:
        """
        オプション戦略注文（マルチレッグ注文）をキャンセル

        :param multileg_order_id: マルチレッグ注文ID
        :return: キャンセルレスポンス
        """
        params = {"AccountKey": self.account_key}
        r = mo.CancelMultilegOrder(MultiLegOrderId=multileg_order_id, params=params)
        return self.client.request(r)

    # ========== カスタム戦略構築ヘルパー ==========

    def create_leg(
        self,
        uic: int,
        amount: int,
        buy_sell: str,
        to_open_close: str,
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        カスタム戦略用のレグ情報（辞書）を作成

        :param uic: Uic
        :param amount: 数量（常に正の値）
        :param buy_sell: "Buy" or "Sell"
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param asset_type: 資産タイプ (Default: StockOption)
        :return: レグ辞書
        """
        return {
            "Uic": uic,
            "Amount": abs(amount),
            "BuySell": buy_sell,
            "AssetType": asset_type,
            "ToOpenClose": to_open_close,
            **kwargs,
        }

    def create_call_leg(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        action: str = "Buy",
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワード検索からCallオプションのレグを作成

        :param keyword: 検索キーワード (例: "AMD")
        :param expiry_date: 満期日 (YYYY-MM-DD)
        :param strike_price: 行使価格
        :param amount: 数量
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param action: "Buy" or "Sell" (Default: Buy)
        :param asset_type: 資産タイプ (Default: StockOption)
        :return: レグ辞書
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Call", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Call")

        return self.create_leg(
            uic=option.uic,
            amount=amount,
            buy_sell=action,
            to_open_close=to_open_close,
            asset_type=asset_type,
            **kwargs,
        )

    def create_put_leg(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        amount: int,
        to_open_close: str,
        action: str = "Buy",
        asset_type: str = "StockOption",
        **kwargs,
    ) -> dict[str, Any]:
        """
        キーワード検索からPutオプションのレグを作成

        :param keyword: 検索キーワード (例: "AMD")
        :param expiry_date: 満期日 (YYYY-MM-DD)
        :param strike_price: 行使価格
        :param amount: 数量
        :param to_open_close: "ToOpen" or "ToClose"（必須）
        :param action: "Buy" or "Sell" (Default: Buy)
        :param asset_type: 資産タイプ (Default: StockOption)
        :return: レグ辞書
        """
        option = self.finder.find_option(keyword, expiry_date, strike_price, "Put", asset_type)
        if option is None:
            raise ValueError(f"Option not found: {keyword} {expiry_date} {strike_price} Put")

        return self.create_leg(
            uic=option.uic,
            amount=amount,
            buy_sell=action,
            to_open_close=to_open_close,
            asset_type=asset_type,
            **kwargs,
        )
