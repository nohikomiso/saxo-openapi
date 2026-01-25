# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, Union

import saxo_openapi.definitions.orders as OD

from .baseorder import BaseOrder
from .helper import direction_from_amount, tie_account_to_order


class MarketCloseOrder(BaseOrder):
    """create a MarketCloseOrder (Explicit Close).

    MarketCloseOrder is used to build the body for a specific position closure.
    It constructs the complex nested structure required by the Saxo API for
    explicit closes:

    {
        "PositionId": "...",
        "Orders": [
            {
                "Uic": ...,
                "AssetType": ...,
                "Amount": ...,
                "OrderType": "Market",
                ...
            }
        ]
    }
    """

    def __init__(
        self,
        PositionId: str,
        Uic: int,
        Amount: Union[int, float],
        AssetType: str,
        BuySell: Optional[str] = None,
        OrderType: str = OD.OrderType.Market,
        AmountType: str = OD.AmountType.Quantity,
        ManualOrder: bool = False,
        ExternalReference: Optional[str] = None,
        TakeProfitOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        StopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
        TrailingStopLossOnFill: Optional[Union[Dict[str, Any], Any]] = None,
    ) -> None:
        """
        Instantiate a MarketCloseOrder.

        Parameters
        ----------
        PositionId: str (required)
            The ID of the position to close.

        Uic: int (required)
            The Uic of the instrument to trade.

        Amount: decimal (required)
            The amount to close. Positive value implies Buy, Negative implies Sell
            if BuySell is not provided.

        AssetType: string (required)
            The asset type for the Uic.

        BuySell: string (optional)
            "Buy" or "Sell". If not provided, it is inferred from the sign of Amount.
            Note: To close a Long position, you generally Sell (Amount < 0 or BuySell="Sell").
            To close a Short position, you generally Buy (Amount > 0 or BuySell="Buy").

        OrderType: string (optional)
            Defaults to "Market".

        AmountType: string (optional)
            Defaults to "Quantity".

        ManualOrder: bool (optional)
            Defaults to False.

        ExternalReference: str (optional)
            Free text reference.

        TakeProfitOnFill, StopLossOnFill, TrailingStopLossOnFill: optional
            Related orders.
        """
        super(MarketCloseOrder, self).__init__()

        # 1. Prepare the inner Order object
        order_details = {
            "Uic": Uic,
            "AssetType": AssetType,
            "Amount": abs(Amount),
            "OrderType": OrderType,
            "AmountType": AmountType,
            "ManualOrder": ManualOrder,
            "OrderDuration": {"DurationType": OD.OrderDurationType.DayOrder},
        }

        # Determine BuySell direction
        if BuySell:
            order_details["BuySell"] = BuySell
        else:
            order_details["BuySell"] = direction_from_amount(Amount)

        if ExternalReference:
            order_details["ExternalReference"] = ExternalReference

        # Handle related orders using the mixin logic manually or by adding keys
        # The base helper/mixin usually adds these to self._data, but here we need them
        # inside the nested order details.

        # We can reuse the OnFillHnd mixin's logic if we inherited from it, but
        # since we are nesting, it's cleaner to just add them if present.
        if TakeProfitOnFill:
            order_details["TakeProfitOnFill"] = (
                TakeProfitOnFill
                if isinstance(TakeProfitOnFill, dict)
                else TakeProfitOnFill.data
            )
        if StopLossOnFill:
            order_details["StopLossOnFill"] = (
                StopLossOnFill
                if isinstance(StopLossOnFill, dict)
                else StopLossOnFill.data
            )
        if TrailingStopLossOnFill:
            order_details["TrailingStopLossOnFill"] = (
                TrailingStopLossOnFill
                if isinstance(TrailingStopLossOnFill, dict)
                else TrailingStopLossOnFill.data
            )

        # 2. Construct the outer structure
        self._data = {
            "PositionId": PositionId,
            "Orders": [order_details],
        }

    @property
    def data(self):
        """data property.

        return the JSON body.
        """
        # Ensure deep copy behavior if needed, or simply return as is since BaseOrder.data
        # logic handles the update loop which works fine for top-level keys.
        # But BaseOrder.data() iterates and filters None. Our structure is fixed.
        # Let's delegate to BaseOrder.data which does the right thing (strips None).

        # Actually, BaseOrder.data implementation:
        # for k, v in self._data.items():
        #     if v is None: continue
        #     d.update({k: v})
        # This will work for "PositionId" and "Orders".

        return super(MarketCloseOrder, self).data
