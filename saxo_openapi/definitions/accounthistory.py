# -*- coding: utf-8 -*-
"""AccountHistory Definitions."""


class InlineCountValue:
    """Definition representation of InlineCountValue"""

    AllPages = "AllPages"
    None_ = "None"

    def __init__(self):
        self._definitions = {
            "AllPages": "The results will contain a total count of items in the queried dataset.",
            "None": "The results will not contain an inline count.",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class AccountPerformanceStandardPeriod:
    """Definition representation of AccountPerformanceStandardPeriod"""

    AllTime = "AllTime"
    Month = "Month"
    Quarter = "Quarter"
    Year = "Year"

    def __init__(self):
        self._definitions = {
            "AllTime": "All time account performance.",
            "Month": "The month standard account performance.",
            "Quarter": "The quarter standard account performance.",
            "Year": "The year standard account performance.",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class AssetType:
    """Definition representation of AssetType"""

    Name = "Name"
    Bond = "Bond"
    Cash = "Cash"
    CfdIndexOption = "CfdIndexOption"
    CfdOnFutures = "CfdOnFutures"
    CfdOnIndex = "CfdOnIndex"
    CfdOnStock = "CfdOnStock"
    ContractFutures = "ContractFutures"
    FuturesOption = "FuturesOption"
    FuturesStrategy = "FuturesStrategy"
    FxBinaryOption = "FxBinaryOption"
    FxForwards = "FxForwards"
    FxKnockInOption = "FxKnockInOption"
    FxKnockOutOption = "FxKnockOutOption"
    FxNoTouchOption = "FxNoTouchOption"
    FxOneTouchOption = "FxOneTouchOption"
    FxSpot = "FxSpot"
    FxVanillaOption = "FxVanillaOption"
    ManagedFund = "ManagedFund"
    MutualFund = "MutualFund"
    Stock = "Stock"
    StockIndex = "StockIndex"
    StockIndexOption = "StockIndexOption"
    StockOption = "StockOption"

    def __init__(self):
        self._definitions = {
            "Name": "Description",
            "Bond": "Bond.",
            "Cash": "Cash. Not tradeable!",
            "CfdIndexOption": "Cfd Index Option.",
            "CfdOnFutures": "Cfd on Futures.",
            "CfdOnIndex": "Cfd on Stock Index.",
            "CfdOnStock": "Cfd on Stock.",
            "ContractFutures": "Contract Futures.",
            "FuturesOption": "Futures Option.",
            "FuturesStrategy": "Futures Strategy.",
            "FxBinaryOption": "Forex Binary Option.",
            "FxForwards": "Forex Forward.",
            "FxKnockInOption": "Forex Knock In Option.",
            "FxKnockOutOption": "Forex Knock Out Option.",
            "FxNoTouchOption": "Forex No Touch Option.",
            "FxOneTouchOption": "Forex One Touch Option.",
            "FxSpot": "Forex Spot.",
            "FxVanillaOption": "Forex Vanilla Option.",
            "ManagedFund": "Obsolete: Managed Fund.",
            "MutualFund": "Mutual Fund.",
            "Stock": "Stock.",
            "StockIndex": "Stock Index.",
            "StockIndexOption": "Stock Index Option.",
            "StockOption": "Stock Option.",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class AccountPerformanceFieldGroup:
    """Definition representation of AccountPerformanceFieldGroup"""

    AccountSummary = "AccountSummary"
    All = "All"
    Allocation = "Allocation"
    AvailableBenchmarks = "AvailableBenchmarks"
    BalancePerformance = "BalancePerformance"
    BalancePerformance_AccountValueTimeSeries = (
        "BalancePerformance_AccountValueTimeSeries"
    )
    BenchMark = "BenchMark"
    BenchmarkPerformance = "BenchmarkPerformance"
    TimeWeightedPerformance = "TimeWeightedPerformance"
    TimeWeightedPerformance_AccumulatedTimeWeightedTimeSeries = (
        "TimeWeightedPerformance_AccumulatedTimeWeightedTimeSeries"
    )
    TotalCashBalancePerCurrency = "TotalCashBalancePerCurrency"
    TotalPositionsValuePerCurrency = "TotalPositionsValuePerCurrency"
    TotalPositionsValuePerProductPerSecurity = (
        "TotalPositionsValuePerProductPerSecurity"
    )
    TradeActivity = "TradeActivity"

    def __init__(self):
        self._definitions = {
            "AccountSummary": "",
            "All": "",
            "Allocation": "",
            "AvailableBenchmarks": "",
            "BalancePerformance": "",
            "BalancePerformance_AccountValueTimeSeries": "",
            "BenchMark": "",
            "BenchmarkPerformance": "",
            "TimeWeightedPerformance": "",
            "TimeWeightedPerformance_AccumulatedTimeWeightedTimeSeries": "",
            "TotalCashBalancePerCurrency": "",
            "TotalPositionsValuePerCurrency": "",
            "TotalPositionsValuePerProductPerSecurity": "",
            "TradeActivity": "",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]
