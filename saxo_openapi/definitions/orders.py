"""Order related definitions."""


class AmountType:
    """Definition representation of AmountType"""

    CashAmount = "CashAmount"
    Quantity = "Quantity"

    def __init__(self):
        self._definitions = {
            "CashAmount": "Order amount is specified as a monetary value",
            "Quantity": "Order Amount is specified as an amount of lots/shares/contracts",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class AssetType:
    """Definition representation of AssetType"""

    Bond = "Bond"
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
            "Bond": "Bond",
            "CfdIndexOption": "Cfd Index Option",
            "CfdOnFutures": "Cfd on Futures",
            "CfdOnIndex": "Cfd on Stock Index",
            "CfdOnStock": "Cfd on Stock",
            "ContractFutures": "Contract Futures",
            "FuturesOption": "Futures Option",
            "FuturesStrategy": "Futures Strategy",
            "FxBinaryOption": "Forex Binary Option",
            "FxForwards": "Forex Forward",
            "FxKnockInOption": "Forex Knock In Option",
            "FxKnockOutOption": "Forex Knock Out Option",
            "FxNoTouchOption": "Forex No Touch Option",
            "FxOneTouchOption": "Forex One Touch Option",
            "FxSpot": "Forex Spot",
            "FxVanillaOption": "Forex Vanilla Option",
            "ManagedFund": "Obsolete: Managed Fund",
            "MutualFund": "Mutual Fund",
            "Stock": "Stock",
            "StockIndex": "Stock Index",
            "StockIndexOption": "Stock Index Option",
            "StockOption": "Stock Option",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class Direction:
    """Definition representation of Direction"""

    Buy = "Buy"
    Sell = "Sell"

    def __init__(self):
        self._definitions = {
            "Buy": "Buy",
            "Sell": "Sell",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class OrderDurationType:
    """Definition representation of OrderDurationType"""

    AtTheClose = "AtTheClose"
    AtTheOpening = "AtTheOpening"
    DayOrder = "DayOrder"
    FillOrKill = "FillOrKill"
    GoodForPeriod = "GoodForPeriod"
    GoodTillCancel = "GoodTillCancel"
    GoodTillDate = "GoodTillDate"
    ImmediateOrCancel = "ImmediateOrCancel"

    def __init__(self):
        self._definitions = {
            "AtTheClose": "At the close of the trading session",
            "AtTheOpening": "At the Opening of the trading session",
            "DayOrder": "Day order - Valid for the trading session",
            "FillOrKill": "Fill or Kill order",
            "GoodForPeriod": "Good for Period",
            "GoodTillCancel": "Good til Cancel",
            "GoodTillDate": "Good til Date",
            "ImmediateOrCancel": "Immediate or Cancel",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class OrderType:
    """Definition representation of OrderType"""

    Algorithmic = "Algorithmic"
    Limit = "Limit"
    Market = "Market"
    Stop = "Stop"
    StopIfTraded = "StopIfTraded"
    StopLimit = "StopLimit"
    Switch = "Switch"
    TrailingStop = "TrailingStop"
    TrailingStopIfBid = "TrailingStopIfBid"
    TrailingStopIfOffered = "TrailingStopIfOffered"
    TrailingStopIfTraded = "TrailingStopIfTraded"
    Traspaso = "Traspaso"
    TraspasoIn = "TraspasoIn"

    def __init__(self):
        self._definitions = {
            "Algorithmic": "Algo order",
            "Limit": "Limit Order",
            "Market": "Market Order",
            "Stop": "Stop Order",
            "StopIfTraded": "Stop if traded",
            "StopLimit": "Stop Limit Order",
            "Switch": "Switch order, Sell X and Buy Y with one order",
            "TrailingStop": "Trailing stop",
            "TrailingStopIfBid": "Trailing stop if bid",
            "TrailingStopIfOffered": "Trailing stop if offered",
            "TrailingStopIfTraded": "Trailing stop if traded",
            "Traspaso": "Traspaso. Specific type of switch order. Only available on select MutualFunds",
            "TraspasoIn": "TraspasoIn. Specific type of switch order",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class ToOpenClose:
    """Definition representation of ToOpenClose"""

    ToClose = "ToClose"
    ToOpen = "ToOpen"
    Undefined = "Undefined"

    def __init__(self):
        self._definitions = {
            "ToClose": "Order/Position is ToClose",
            "ToOpen": "Order/Position is ToOpen",
            "Undefined": "Undefined",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]
