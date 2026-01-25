# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Union

import saxo_openapi.definitions.orders as OD

from .baseorder import BaseOrder
from .helper import direction_from_amount, order_duration_spec
from .mixin import OnFillHnd


class StopLimitOrder(BaseOrder, OnFillHnd):
    """create a StopLimitOrder.

    StopLimitOrder is used to build the body for a StopLimitOrder. The body can be
    used to pass to the Order endpoint.
    """

    # allowed OrderDurationTypes:
    ALLOWED_DT: ClassVar[List[str]] = [
        OD.OrderDurationType.DayOrder,
        OD.OrderDurationType.GoodTillDate,
        OD.OrderDurationType.GoodTillCancel,
    ]

    def __init__(
        self,
        Uic: int,
        Amount: Union[int, float],
        AssetType: str,
        OrderPrice: Union[int, float],
        StopLimitPrice: Union[int, float],
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        StopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        TrailingStopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        ExternalReference: Optional[str] = None,
        IsForceOpen: bool = True,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: Optional[Union[str, datetime]] = None,
    ) -> None:
        """
        Instantiate a StopLimitOrder.

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
            the price indicating the stop trigger price

        StopLimitPrice: decimal (required)
            the price indicating the limit price after trigger

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
        >>> from saxo_openapi.contrib.orders import StopLimitOrder
        >>> # create a stop limit order for AAPL CFD (Uic=211)
        >>> slo = StopLimitOrder(Uic=211,
        ...                      AssetType=OD.AssetType.CfdOnStock,
        ...                      Amount=1,
        ...                      OrderPrice=150.0,
        ...                      StopLimitPrice=149.5,
        ...                      ExternalReference="stop_limit_order_123")
        >>> print(json.dumps(slo.data, indent=4))
        {
          "Uic": 211,
          "AssetType": "CfdOnStock",
          "Amount": 1,
          "BuySell": "Buy",
          "OrderType": "StopLimit",
          "OrderPrice": 150.0,
          "StopLimitPrice": 149.5,
          "AmountType": "Quantity",
          "ManualOrder": false,
          "ExternalReference": "stop_limit_order_123",
          "IsForceOpen": true,
          "OrderDuration": {
              "DurationType": "DayOrder"
          }
        }
        >>> # now we have the order specification, create the order request
        >>> r = tr.orders.Order(data=slo.data)
        >>> # perform the request
        >>> rv = client.request(r)
        >>> print(rv)
        """

        super(StopLimitOrder, self).__init__()

        # by default for a StopLimitOrder
        da: Dict[str, Any] = {
            "OrderType": OD.OrderType.StopLimit,
            "AmountType": AmountType,
        }

        da.update(
            {
                "OrderDuration": order_duration_spec(
                    OrderDurationType, self.ALLOWED_DT, GTDDate
                )
            }
        )

        # required
        self._data.update({"Uic": Uic})
        self._data.update({"AssetType": AssetType})
        self._data.update({"Amount": abs(Amount)})
        self._data.update({"ManualOrder": ManualOrder})
        self._data.update({"OrderPrice": OrderPrice})
        self._data.update({"StopLimitPrice": StopLimitPrice})
        self._data.update({"BuySell": direction_from_amount(Amount)})
        self._data.update(da)

        # optional parameters
        if ExternalReference is not None:
            self._data.update({"ExternalReference": ExternalReference})
        if IsForceOpen is not None:
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
        return super(StopLimitOrder, self).data


class StopLimitOrderCfdOnStock(StopLimitOrder):
    """StopLimitOrderCfdOnStock - StopLimitOrder for CfdOnStock only.

    The StopLimitOrderCfdOnStock lacks the AssetType parameter and only serves
    the AssetType CfdOnStock.
    """

    def __init__(
        self,
        Uic: int,
        Amount: Union[int, float],
        OrderPrice: Union[int, float],
        StopLimitPrice: Union[int, float],
        ManualOrder: bool = False,
        AmountType: str = OD.AmountType.Quantity,
        TakeProfitOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        StopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        TrailingStopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        ExternalReference: Optional[str] = None,
        IsForceOpen: bool = True,
        OrderDurationType: str = OD.OrderDurationType.DayOrder,
        GTDDate: Optional[Union[str, datetime]] = None,
    ) -> None:
        """
        Instantiate a StopLimitOrderCfdOnStock.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount. A value > 0 means 'buy',
            a value < 0 means 'sell'

        OrderPrice: decimal (required)
            the price indicating the stop trigger price

        StopLimitPrice: decimal (required)
            the price indicating the limit price after trigger

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
        >>> from saxo_openapi.contrib.orders import tie_account_to_order, StopLimitOrderCfdOnStock
        >>> # create a stop limit order for AAPL CFD (Uic=211)
        >>> order = tie_account_to_order(
        ...     AccountKey,
        ...     StopLimitOrderCfdOnStock(Uic=211,
        ...                              Amount=1,
        ...                              OrderPrice=150.0,
        ...                              StopLimitPrice=149.5,
        ...                              ExternalReference="PythonCLIOrder1234"))
        >>> r = tr.orders.Order(data=order)
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))
        {
          "OrderId": "12345678"
        }
        """
        super(StopLimitOrderCfdOnStock, self).__init__(
            Uic=Uic,
            Amount=Amount,
            OrderPrice=OrderPrice,
            StopLimitPrice=StopLimitPrice,
            ManualOrder=ManualOrder,
            AmountType=AmountType,
            AssetType=OD.AssetType.CfdOnStock,
            OrderDurationType=OrderDurationType,
            TakeProfitOnFill=TakeProfitOnFill,
            StopLossOnFill=StopLossOnFill,
            TrailingStopLossOnFill=TrailingStopLossOnFill,
            ExternalReference=ExternalReference,
            IsForceOpen=IsForceOpen,
            GTDDate=GTDDate,
        )
