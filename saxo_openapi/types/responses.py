"""レスポンス型定義

このモジュールは、Saxo OpenAPI の主要なレスポンス構造の TypedDict 定義を提供します。
型ヒントにより、AIコード生成時のエラーを削減し、IDE補完を改善します。

実装方針: 主要フィールドのみ定義 (5-10フィールド程度)、完璧主義禁止

See: docs/api/README.md
"""

from typing import TypedDict

# ============================================================================
# Portfolio - Balances
# ============================================================================


class BalanceResponse(TypedDict, total=False):
    """残高レスポンス

    See: docs/schemas/portfolio/balances/account_balances_me_response.json
    """

    CashBalance: float
    Currency: str
    TotalValue: float
    MarginAvailableForTrading: float
    MarginUsedByCurrentPositions: float
    MarginUtilizationPct: float
    OpenPositionsCount: int
    OrdersCount: int


# ============================================================================
# Portfolio - Positions
# ============================================================================


class PositionBaseResponse(TypedDict, total=False):
    """ポジション基本情報

    See: docs/schemas/portfolio/positions/positions_me_response.json
    """

    AccountId: str
    Amount: float
    AssetType: str
    CanBeClosed: bool
    ClientId: str
    OpenPrice: float
    SourceOrderId: str
    Status: str
    Uic: int


class PositionViewResponse(TypedDict, total=False):
    """ポジション表示情報

    See: docs/schemas/portfolio/positions/positions_me_response.json
    """

    CurrentPrice: float
    CurrentPriceType: str
    Exposure: float
    ExposureCurrency: str
    ExposureInBaseCurrency: float
    ProfitLossOnTrade: float
    ProfitLossOnTradeInBaseCurrency: float


class PositionResponse(TypedDict, total=False):
    """ポジションレスポンス

    See: docs/schemas/portfolio/positions/positions_me_response.json
    """

    PositionId: str
    NetPositionId: str
    PositionBase: PositionBaseResponse
    PositionView: PositionViewResponse


# ============================================================================
# Portfolio/Trading - Orders
# ============================================================================


class OrderResponse(TypedDict, total=False):
    """注文レスポンス

    See: docs/schemas/portfolio/orders/get_open_orders_me_response.json
    """

    OrderId: str
    AccountId: str
    AccountKey: str
    Amount: float
    AssetType: str
    BuySell: str
    ClientKey: str
    CurrentPrice: float
    OpenOrderType: str
    OrderTime: str
    Price: float
    Status: str
    Uic: int
