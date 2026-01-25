"""Option trading data types."""

from dataclasses import dataclass, field


@dataclass
class OptionRoot:
    """オプションルート（オプション銘柄の基盤）

    GET /ref/v1/instruments (AssetTypes=StockOption) で取得。
    SummaryType が "ContractOptionRoot" のエントリから生成。
    """

    option_root_id: int  # Identifier from search result
    symbol: str  # "AMD:xnas"
    description: str  # "Advanced Micro Devices Inc"
    asset_type: str  # "StockOption", "StockIndexOption"
    currency_code: str  # "USD"
    exchange_id: str  # "CBOE" など
    can_participate_in_multileg: bool = False


@dataclass
class ExpiryInfo:
    """満期日情報

    ContractOptionSpaces のレスポンスから生成。
    """

    display_expiry: str  # 表示用 "2026-02-01"
    expiry: str  # 実際の満期日 "2026-02-06"
    last_trade_date: str  # 最終取引日時
    days_to_expiry: int  # 満期までの日数


@dataclass
class OptionContract:
    """個別オプション契約

    ContractOptionSpaces の SpecificOptions から生成。
    このUicを使って注文を発注する。
    """

    uic: int  # 注文に使うUic
    strike_price: float  # 行使価格
    put_call: str  # "Call" or "Put"
    expiry: str  # 満期日
    underlying_uic: int  # 原資産のUic（参考用、注文には不要）


@dataclass
class OptionChain:
    """オプションチェーン（満期日別のオプション一覧）

    ContractOptionSpaces のレスポンスから生成。
    """

    option_root_id: int
    asset_type: str
    description: str
    contract_size: float
    exercise_style: str  # "American" or "European"
    settlement_style: str  # "Cash" or "PhysicalDelivery"
    supported_order_types: list[str] = field(default_factory=list)
    expiries: list[ExpiryInfo] = field(default_factory=list)
    calls: list[OptionContract] = field(default_factory=list)
    puts: list[OptionContract] = field(default_factory=list)


class OptionsStrategyType:
    """オプション戦略タイプ"""

    VERTICAL = "Vertical"
    CALENDAR_SPREAD = "CalendarSpread"
    DIAGONAL = "Diagonal"
    STRADDLE = "Straddle"
    STRANGLE = "Strangle"
    BUTTERFLY = "Butterfly"
    IRON_BUTTERFLY = "IronButterfly"
    CONDOR = "Condor"
    IRON_CONDOR = "IronCondor"
    BACK_RATIO = "BackRatio"
    RISK_REVERSAL = "RiskReversal"
    COMBO = "Combo"
    SYNTHETIC = "Synthetic"
    GUT = "Gut"
    CUSTOM = "Custom"
