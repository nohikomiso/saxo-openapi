from datetime import datetime
from typing import Any, ClassVar

import saxo_openapi.definitions.orders as OD

from .baseorder import BaseOrder
from .helper import direction_from_amount, order_duration_spec
from .mixin import OnFillHnd


class StopOrder(BaseOrder, OnFillHnd):
    """create a StopOrder.

    StopOrder is used to build the body for a StopOrder. The body can be
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
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: dict[str, Any] | Any | None = None,
        StopLossOnFill: dict[str, Any] | Any | None = None,
        TrailingStopLossOnFill: dict[str, Any] | Any | None = None,
        ExternalReference: str | None = None,
        IsForceOpen: bool = True,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: str | datetime | None = None,
    ) -> None:
        """
        Instantiate a StopOrder.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount. A value > 0 means 'buy',
            a value < 0 means 'sell'

        AssetType: string (required)
            the assettype for the Uic

        OrderPrice: decimal (required)
            the price indicating the stop price

        ManualOrder: bool (required)
            flag to identify if an order is from an automated origin,
            default: False

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for
            other options

        ExternalReference: str (optional)
            A free text reference to identify the order. This can be used to
            associate the order with an external system or reference.

        IsForceOpen: bool (optional)
            If True, opens a new position even if there's an opposite position.
            If False, the order will be netted against any existing opposite position.
            Default: True

        TakeProfitOnFill: TakeProfitDetails instance or dict
            the take-profit order specification

        StopLossOnFill: StopLossDetails instance or dict
            the stoploss order specification

        TrailingStopLossOnFill: TrailingStopLossDetails instance or dict
            the Trailingstoploss order specification

        OrderDurationType: OrderDurationType (optional)
            The duration type for the order. Must be one of:
            - DayOrder: Order is valid for the trading day
            - GoodTillDate: Order is valid until the specified GTD date
            - GoodTillCancel: Order remains valid until cancelled
            Default: DayOrder

        GTDDate: datetime (optional)
            Required if OrderDurationType is GoodTillDate. The date until
            which the order remains valid.

        Example
        -------

        >>> import json
        >>> from saxo_openapi import API
        >>> import saxo_openapi.endpoints.trading as tr
        >>> from saxo_openapi.contrib.orders import StopOrder
        >>> # create a stop order for EURUSD (Uic=21)
        >>> so = StopOrder(Uic=21,
        ...                AssetType=OD.AssetType.FxSpot,
        ...                Amount=10000,
        ...                OrderPrice=1.1000,
        ...                ExternalReference="stop_order_123")
        >>> print(json.dumps(so.data, indent=4))
        {
          "Uic": 21,
          "AssetType": "FxSpot",
          "Amount": 10000,
          "BuySell": "Buy",
          "OrderType": "Stop",
          "OrderPrice": 1.1000,
          "AmountType": "Quantity",
          "ManualOrder": False,
          "ExternalReference": "stop_order_123",
          "OrderDuration": {
              "DurationType": "DayOrder"
          }
        }
        >>> # now we have the order specification, create the order request
        >>> r = tr.orders.Order(data=so.data)
        >>> # perform the request
        >>> rv = client.request(r)
        >>> print(rv)

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        AssetType: string (required)
            the assettype for the Uic

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
        >>> from saxo_openapi.contrib.orders import StopOrder
        >>>
        >>> so = StopOrder(Uic=21,
                         AssetType=OD.AssetType.FxSpot,
                         Amount=10000,
                         OrderPrice=1.1025)
        >>> print(json.dumps(so.data, indent=2))
        {
          "Uic": 21,
          "AssetType": "FxSpot",
          "Amount": 10000,
          "Price": 1.1025,
          "BuySell": "Buy",
          "OrderType": "Stop",
          "ManualOrder": false,
          "AmountType": "Quantity",
          "OrderDuration": {
             "DurationType": "DayOrder"
          }
        }
        >>> # now we have the order specification, create the order request
        >>> r = tr.orders.Order(data=so.data)
        >>> # perform the request
        >>> rv = client.request(r)
        >>> print(rv)
        >>> print(json.dumps(rv, indent=4))
        {
           "OrderId": "76697286"
        }
        """

        super(StopOrder, self).__init__()

        # by default for a StopOrder
        da: dict[str, Any] = {
            "OrderType": OD.OrderType.Stop,
            "AmountType": AmountType,
        }

        da.update({"OrderDuration": order_duration_spec(OrderDurationType, self.ALLOWED_DT, GTDDate)})

        # required
        self._data.update({"Uic": Uic})
        self._data.update({"AssetType": AssetType})
        self._data.update({"Amount": abs(Amount)})
        self._data.update({"ManualOrder": ManualOrder})
        self._data.update({"OrderPrice": OrderPrice})
        self._data.update({"BuySell": direction_from_amount(Amount)})
        self._data.update(da)

        # optional
        if ExternalReference is not None:
            self._data.update({"ExternalReference": ExternalReference})

        self._data.update({"IsForceOpen": IsForceOpen})

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
        return super(StopOrder, self).data


class StopOrderFxSpot(StopOrder):
    """StopOrderFxSpot - StopOrder for FxSpot only.

    The StopOrderFxSpot lacks the AssetType parameter and only serves
    the AssetType FxSpot.
    """

    def __init__(
        self,
        Uic: int,
        Amount: int | float,
        OrderPrice: int | float,
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: dict[str, Any] | Any | None = None,
        StopLossOnFill: dict[str, Any] | Any | None = None,
        TrailingStopLossOnFill: dict[str, Any] | Any | None = None,
        ExternalReference: str | None = None,
        IsForceOpen: bool = True,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: str | datetime | None = None,
    ) -> None:
        """
        Instantiate a StopOrderFxSpot.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        ManualOrder: bool (required)
            flag to identify if an order is from an automated origin,
            default: False

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for

        ExternalReference: str (optional)
            A free text reference to identify the order. This can be used to
            associate the order with an external system or reference.

        IsForceOpen: bool (optional)
            If True, opens a new position even if there's an opposite position.
            If False, the order will be netted against any existing opposite position.
            Default: True

        TakeProfitOnFill: TakeProfitDetails instance or dict
            the take-profit order specification

        StopLosstOnFill: StopLossDetails instance or dict
            the stoploss order specification

        TrailingStopLosstOnFill: TrailingStopLossDetails instance or dict
            the Trailingstoploss order specification
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

        >>> from saxo_openapi import API
        >>> from saxo_openapi.contrib.orders import (
        ...          tie_account_to_order,
        ...          StopOrderFxSpot)
        >>> token = "..."
        >>> client = API(access_token=token)
        >>> order = tie_account_to_order(
        ...     AccountKey,
        ...     StopOrderFxSpot(Uic=21, Amount=25000, OrderPrice=1.1025))
        >>> r = tr.orders.Order(data=order)
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))
        {
          "OrderId": "76703544"
        }
        """
        super(StopOrderFxSpot, self).__init__(
            Uic=Uic,
            Amount=Amount,
            OrderPrice=OrderPrice,
            ManualOrder=ManualOrder,
            AmountType=AmountType,
            AssetType=OD.AssetType.FxSpot,
            TakeProfitOnFill=TakeProfitOnFill,
            StopLossOnFill=StopLossOnFill,
            TrailingStopLossOnFill=TrailingStopLossOnFill,
            ExternalReference=ExternalReference,
            IsForceOpen=IsForceOpen,
            OrderDurationType=OrderDurationType,
            GTDDate=GTDDate,
        )
