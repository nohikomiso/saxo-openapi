"""Option finder helper for searching and discovering option contracts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import saxo_openapi.endpoints.referencedata as rd
from saxo_openapi.contrib.option_types import (
    ExpiryInfo,
    OptionChain,
    OptionContract,
    OptionRoot,
)
from saxo_openapi.contrib.session import account_info

if TYPE_CHECKING:
    from saxo_openapi import API


class OptionFinder:
    """オプション契約の検索を支援するヘルパークラス

    オプション注文を発注するために必要な情報（オプション契約のUic）を
    取得するためのメソッドを提供します。

    使用フロー:
    1. search_option_roots() でオプションルートを検索
    2. get_option_chain() でオプションチェーンを取得
    3. チェーン内のオプション契約から目的のUicを取得
    4. そのUicを使って OptionTrader で注文を発注
    """

    def __init__(self, client: API, account_key: str | None = None):
        """
        OptionFinder を初期化

        :param client: APIクライアント
        :param account_key: アカウントキー（Noneの場合は自動取得）
        """
        self.client = client
        self._account_key = account_key

    @property
    def account_key(self) -> str:
        """AccountKey を取得（必要に応じて自動取得）"""
        if self._account_key is None:
            self._account_key = account_info(self.client).AccountKey
        return self._account_key

    def search_option_roots(
        self,
        keyword: str,
        asset_type: str = "StockOption",
        exchange_id: str | None = None,
    ) -> list[OptionRoot]:
        """
        オプションルートを検索

        :param keyword: 検索キーワード（例: "AMD", "SPY", "AAPL"）
        :param asset_type: 資産タイプ（"StockOption" or "StockIndexOption"）
        :param exchange_id: 取引所ID（任意。例: "CBOE"）
        :return: オプションルートのリスト

        使用API: GET /ref/v1/instruments
        """
        params: dict[str, Any] = {
            "AccountKey": self.account_key,
            "Keywords": keyword,
            "AssetTypes": asset_type,
        }
        if exchange_id:
            params["ExchangeId"] = exchange_id

        r = rd.instruments.Instruments(params=params)
        response = self.client.request(r)

        results = []
        for item in response.get("Data", []):
            # ContractOptionRoot タイプのみを処理
            if item.get("SummaryType") == "ContractOptionRoot":
                results.append(
                    OptionRoot(
                        option_root_id=item.get("Identifier"),
                        symbol=item.get("Symbol", ""),
                        description=item.get("Description", ""),
                        asset_type=item.get("AssetType", ""),
                        currency_code=item.get("CurrencyCode", ""),
                        exchange_id=item.get("ExchangeId", ""),
                        can_participate_in_multileg=item.get("CanParticipateInMultiLegOrder", False),
                    )
                )
        return results

    def get_option_chain(
        self,
        option_root_id: int,
        expiry_dates: list[str] | None = None,
    ) -> OptionChain:
        """
        オプションチェーン（満期日別のオプション契約一覧）を取得

        :param option_root_id: オプションルートID（search_option_roots で取得）
        :param expiry_dates: 取得する満期日のリスト（Noneの場合は全て）
        :return: オプションチェーン

        使用API: GET /ref/v1/instruments/contractoptionspaces/{OptionRootId}
        """
        params: dict[str, Any] = {}
        if expiry_dates:
            params["OptionSpaceSegment"] = "SpecificDates"
            params["ExpiryDates"] = ",".join(expiry_dates)

        r = rd.instruments.ContractoptionSpaces(OptionRootId=str(option_root_id), params=params if params else None)
        response = self.client.request(r)

        # 基本情報を抽出
        chain = OptionChain(
            option_root_id=response.get("OptionRootId", option_root_id),
            asset_type=response.get("AssetType", ""),
            description=response.get("Description", ""),
            contract_size=response.get("ContractSize", 100),
            exercise_style=response.get("ExerciseStyle", ""),
            settlement_style=response.get("SettlementStyle", ""),
            supported_order_types=response.get("SupportedOrderTypes", []),
        )

        # 満期日とオプション契約を抽出
        calls = []
        puts = []
        expiries = []

        for space in response.get("OptionSpace", []):
            expiry = space.get("Expiry", "")
            expiries.append(
                ExpiryInfo(
                    display_expiry=space.get("DisplayExpiry", ""),
                    expiry=expiry,
                    last_trade_date=space.get("LastTradeDate", ""),
                    days_to_expiry=space.get("DisplayDaysToExpiry", 0),
                )
            )

            for option in space.get("SpecificOptions", []):
                contract = OptionContract(
                    uic=option.get("Uic"),
                    strike_price=option.get("StrikePrice", 0.0),
                    put_call=option.get("PutCall", ""),
                    expiry=expiry,
                    underlying_uic=option.get("UnderlyingUic", 0),
                )
                if contract.put_call == "Call":
                    calls.append(contract)
                elif contract.put_call == "Put":
                    puts.append(contract)

        chain.expiries = expiries
        chain.calls = calls
        chain.puts = puts

        return chain

    def get_expiry_dates(self, option_root_id: int) -> list[ExpiryInfo]:
        """
        利用可能な満期日一覧を取得

        :param option_root_id: オプションルートID
        :return: 満期日情報のリスト
        """
        chain = self.get_option_chain(option_root_id)
        return chain.expiries

    def find_option(
        self,
        keyword: str,
        expiry_date: str,
        strike_price: float,
        put_call: str,
        asset_type: str = "StockOption",
    ) -> OptionContract | None:
        """
        キーワードから特定のオプション契約を一括検索

        :param keyword: 検索キーワード（例: "AMD"）
        :param expiry_date: 満期日（YYYY-MM-DD形式）
        :param strike_price: 行使価格
        :param put_call: "Call" or "Put"
        :param asset_type: 資産タイプ
        :return: マッチしたオプション契約（見つからない場合はNone）
        """
        # Step 1: オプションルートを検索
        roots = self.search_option_roots(keyword, asset_type)
        if not roots:
            return None

        # 最初にマッチしたルートを使用
        root = roots[0]

        # Step 2: オプションチェーンを取得
        chain = self.get_option_chain(root.option_root_id, expiry_dates=[expiry_date])

        # Step 3: 条件に一致するオプションを探す
        options = chain.calls if put_call == "Call" else chain.puts
        for option in options:
            if abs(option.strike_price - strike_price) < 0.01 and option.expiry == expiry_date:
                return option

        return None

    def get_atm_options(
        self,
        option_root_id: int,
        expiry_date: str,
        count: int = 5,
    ) -> dict[str, list[OptionContract]]:
        """
        ATM（アット・ザ・マネー）周辺のオプションを取得

        :param option_root_id: オプションルートID
        :param expiry_date: 満期日
        :param count: ATMから上下何個のオプションを返すか
        :return: {"Call": [...], "Put": [...]}
        """
        chain = self.get_option_chain(option_root_id, expiry_dates=[expiry_date])

        # ストライク価格でソート
        calls_sorted = sorted(chain.calls, key=lambda x: x.strike_price)
        puts_sorted = sorted(chain.puts, key=lambda x: x.strike_price)

        # 中央付近のオプションを取得
        mid_idx_calls = len(calls_sorted) // 2
        mid_idx_puts = len(puts_sorted) // 2

        start_calls = max(0, mid_idx_calls - count)
        end_calls = min(len(calls_sorted), mid_idx_calls + count + 1)
        start_puts = max(0, mid_idx_puts - count)
        end_puts = min(len(puts_sorted), mid_idx_puts + count + 1)

        return {
            "Call": calls_sorted[start_calls:end_calls],
            "Put": puts_sorted[start_puts:end_puts],
        }
