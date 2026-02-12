from datetime import datetime
from typing import Any, ClassVar

import saxo_openapi.definitions.orders as OD

from .baseorder import BaseOrder
from .helper import direction_from_amount, order_duration_spec
from .mixin import OnFillHnd


class LimitOrder(BaseOrder, OnFillHnd):
    """create a LimitOrder.

    LimitOrder is used to build the body for a LimitOrder. The body can be
    used to pass to the Order endpoint.
    """

    # allowed OrderDurationTypes:
    ALLOWED_DT: ClassVar[list[str]] = [
        OD.OrderDurationType.DayOrder,
        OD.OrderDurationType.GoodTillDate,
        OD.OrderDurationType.GoodTillCancel,
    ]

    def __init__(
        self,
        Uic: int,
        Amount: int | float,
        AssetType: str,
        OrderPrice: int | float,
        IsForceOpen: bool,
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: dict[str, Any] | Any | None = None,
        StopLossOnFill: dict[str, Any] | Any | None = None,
        TrailingStopLossOnFill: dict[str, Any] | Any | None = None,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: str | datetime | None = None,
        ExternalReference: str | None = None,
    ) -> None:
        """
        Instantiate a LimitOrder.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        AssetType: string (required)
            the assettype for the Uic

        ExternalReference: str (optional)
            A free text reference to identify the order. This can be used to
            associate the order with an external system or reference.

        IsForceOpen: bool (required)
            Must be explicitly specified. If True, opens a new position even if there's an
            opposite position. If False, the order will be netted against any existing opposite position.

        ManualOrder: bool (required)
            flag to identify if an order is from an automated origin,
            default: False

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for
            other options

        TakeProfitOnFill: TakeProfitDetails instance or dict
            the take-profit order specification

        StopLosstOnFill: StopLossDetails instance or dict
            the stoploss order specification

        TrailingStopLosstOnFill: TrailingStopLossDetails instance or dict
            the Trailingstoploss order specification

        OrderDurationType: string, default DayOrder
            the order duration type, check SAXO Bank specs. for details

        GTDDate: datetime string (required if order duration is GoodTillDate)
            the GTD-datetime

        Example
        -------

        >>> import json
        >>> from saxo_openapi import API
        >>> import saxo_openapi.endpoints.trading as tr
        >>> from saxo_openapi.contrib.orders import LimitOrder
        >>>
        >>> lo = LimitOrder(Uic=21,
        ...                 AssetType=OD.AssetType.FxSpot,
        ...                 Amount=10000,
        ...                 OrderPrice=1.1025)
        >>> print(json.dumps(lo.data, indent=2))
        {
          "Uic": 21,
          "AssetType": "FxSpot",
          "Amount": 10000,
          "Price": 1.1025,
          "BuySell": "Buy",
          "OrderType": "Limit",
          "ManualOrder": false,
          "AmountType": "Quantity",
          "OrderDuration": {
             "DurationType": "DayOrder"
          }
        }
        >>> # Create a LimitOrder with ExternalReference and IsForceOpen
        >>> lo = LimitOrder(
        >>>     Uic=21,
        >>>     Amount=25000,
        >>>     AssetType=OD.AssetType.FxSpot,
        >>>     OrderPrice=1.1025,
        >>>     ManualOrder=False,
        >>>     ExternalReference="ORDER_12345",
        >>>     IsForceOpen=True
        >>> )
        >>> # now we have the order specification, create the order request
        >>> r = tr.orders.Order(data=lo.data)
        >>> # perform the request
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=4))
        {
           "OrderId": "76697286"
        }
        """

        super(LimitOrder, self).__init__()

        # by default for a Limit order
        da: dict[str, Any] = {
            "OrderType": OD.OrderType.Limit,
            "AmountType": AmountType,
        }

        da.update({"OrderDuration": order_duration_spec(OrderDurationType, self.ALLOWED_DT, GTDDate)})

        # required
        self._data.update({"Uic": Uic})
        self._data.update({"AssetType": AssetType})
        self._data.update({"Amount": abs(Amount)})
        self._data.update({"OrderPrice": OrderPrice})
        self._data.update({"BuySell": direction_from_amount(Amount)})
        self._data.update({"ManualOrder": ManualOrder})
        self._data.update(da)

        # optional
        if ExternalReference is not None:
            self._data.update({"ExternalReference": ExternalReference})

        self._data.update({"IsForceOpen": IsForceOpen})

        # Handle possible onFill orders via the mixin
        self.hndOnFill(
            TakeProfitOnFill=TakeProfitOnFill,
            StopLossOnFill=StopLossOnFill,
            TrailingStopLossOnFill=TrailingStopLossOnFill,
        )

    @property
    def data(self):
        """data property.

        return the JSON body.
        """
        return super(LimitOrder, self).data


class LimitOrderFxSpot(LimitOrder):
    """LimitOrderFxSpot - LimitOrder for FxSpot only.

    The LimitOrderFxSpot lacks the AssetType parameter and only serves
    the AssetType FxSpot.
    """

    def __init__(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: int | float,
        IsForceOpen: bool,
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: dict[str, Any] | Any | None = None,
        StopLossOnFill: dict[str, Any] | Any | None = None,
        TrailingStopLossOnFill: dict[str, Any] | Any | None = None,
        ExternalReference: str | None = None,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: str | datetime | None = None,
    ) -> None:
        """
        Instantiate a LimitOrderFxSpot.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for
            other options

        ManualOrder: bool (required)
            flag to identify if an order is from an automated origin,
            default: False

        ExternalReference: str (optional)
            A free text reference to identify the order. This can be used to
            associate the order with an external system or reference.

        IsForceOpen: bool (required)
            Must be explicitly specified. If True, opens a new position even if there's an
            opposite position. If False, the order will be netted against any existing opposite position.

        TakeProfitOnFill: TakeProfitDetails instance or dict
            the take-profit order specification

        StopLosstOnFill: StopLossDetails instance or dict
            the stoploss order specification

        TrailingStopLosstOnFill: TrailingStopLossDetails instance or dict
            the Trailingstoploss order specification

        OrderDurationType: string, default DayOrder
            the order duration type, check SAXO Bank specs. for details

        GTDDate: datetime string (required if order duration is GoodTillDate)
            the GTD-datetime

        Example
        -------

        >>> from saxo_openapi import API
        >>> from saxo_openapi.contrib.orders import (
        ...          tie_account_to_order,
        ...          LimitOrderFxSpot)
        >>> token = "..."
        >>> client = API(access_token=token)
        >>> order = tie_account_to_order(
        ...     AccountKey,
        ...     LimitOrderFxSpot(Uic=21, Amount=25000, OrderPrice=1.1025))
        >>> r = tr.orders.Order(data=order)
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))
        {
          "OrderId": "76703544"
        }
        """
        super(LimitOrderFxSpot, self).__init__(
            Uic=Uic,
            Amount=Amount,
            OrderPrice=OrderPrice,
            AmountType=AmountType,
            ManualOrder=ManualOrder,
            AssetType=OD.AssetType.FxSpot,
            TakeProfitOnFill=TakeProfitOnFill,
            StopLossOnFill=StopLossOnFill,
            TrailingStopLossOnFill=TrailingStopLossOnFill,
            OrderDurationType=OrderDurationType,
            ExternalReference=ExternalReference,
            IsForceOpen=IsForceOpen,
            GTDDate=GTDDate,
        )


class LimitOrderStock(LimitOrder):
    """LimitOrderStock - LimitOrder for Stock only.

    The LimitOrderStock lacks the AssetType parameter and only serves
    the AssetType Stock.
    """

    def __init__(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: int | float,
        AmountType: str = OD.AmountType.Quantity,
        ManualOrder: bool = False,
        TakeProfitOnFill: dict[str, Any] | Any | None = None,
        StopLossOnFill: dict[str, Any] | Any | None = None,
        TrailingStopLossOnFill: dict[str, Any] | Any | None = None,
        ExternalReference: str | None = None,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: str | datetime | None = None,
    ) -> None:
        """
        Instantiate a LimitOrderStock.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for
            other options

        ManualOrder: bool (required)
            flag to identify if an order is from an automated origin,
            default: False

        ExternalReference: str (optional)
            A free text reference to identify the order. This can be used to
            associate the order with an external system or reference.

        IsForceOpen: bool (required)
            Must be explicitly specified. If True, opens a new position even if there's an
            opposite position. If False, the order will be netted against any existing opposite position.

        TakeProfitOnFill: TakeProfitDetails instance or dict
            the take-profit order specification

        StopLosstOnFill: StopLossDetails instance or dict
            the stoploss order specification

        TrailingStopLosstOnFill: TrailingStopLossDetails instance or dict
            the Trailingstoploss order specification

        OrderDurationType: string, default DayOrder
            the order duration type, check SAXO Bank specs. for details

        GTDDate: datetime string (required if order duration is GoodTillDate)
            the GTD-datetime

        Example
        -------

        >>> from saxo_openapi import API
        >>> from saxo_openapi.contrib.orders import (
        ...          tie_account_to_order,
        ...          LimitOrderStock)
        >>> token = "..."
        >>> client = API(access_token=token)
        >>> order = tie_account_to_order(
        ...     AccountKey,
        ...     LimitOrderStock(Uic=16350, Amount=1000, OrderPrice=28.00))
        >>> r = tr.orders.Order(data=order)
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))
        {
          "OrderId": "76703539"
        }
        """
        super(LimitOrderStock, self).__init__(
            Uic=Uic,
            Amount=Amount,
            OrderPrice=OrderPrice,
            AmountType=AmountType,
            ManualOrder=ManualOrder,
            AssetType=OD.AssetType.Stock,
            TakeProfitOnFill=TakeProfitOnFill,
            StopLossOnFill=StopLossOnFill,
            TrailingStopLossOnFill=TrailingStopLossOnFill,
            OrderDurationType=OrderDurationType,
            ExternalReference=ExternalReference,
            IsForceOpen=IsForceOpen,
            GTDDate=GTDDate,
        )
