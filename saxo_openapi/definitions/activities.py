"""Activity related definitions."""


class ActivityType:
    """Definition representation of ActivityType"""

    AccountDepreciation = "AccountDepreciation"
    AccountFundings = "AccountFundings"
    MarginCalls = "MarginCalls"
    Orders = "Orders"
    PositionDepreciation = "PositionDepreciation"
    Positions = "Positions"

    def __init__(self):
        self._definitions = {
            "AccountDepreciation": "Account depreciation information",
            "AccountFundings": "Funding information",
            "MarginCalls": "Margin call information",
            "Orders": "Order related information",
            "PositionDepreciation": "Position depreciation information",
            "Positions": "Position related information",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]


class ActivityFieldGroup:
    """Definition representation of ActivityFieldGroup"""

    DisplayAndFormat = "DisplayAndFormat"
    ExchangeInfo = "ExchangeInfo"

    def __init__(self):
        self._definitions = {
            "DisplayAndFormat": "Display and Format",
            "ExchangeInfo": "Adds information about the instruments's exchange",
        }

    @property
    def definitions(self):
        return self._definitions

    def __getitem__(self, key):
        return self._definitions[key]
