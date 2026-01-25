# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from .helper import direction_invert


class OnFillHnd(object):

    def hndOnFill(
        self,
        TakeProfitOnFill: Optional[Dict[str, Any]] = None,
        StopLossOnFill: Optional[Dict[str, Any]] = None,
        TrailingStopLossOnFill: Optional[Dict[str, Any]] = None,
    ) -> None:

        ospec = None
        for onFillOrder in [TakeProfitOnFill, StopLossOnFill, TrailingStopLossOnFill]:

            if onFillOrder is None:
                continue

            if not isinstance(onFillOrder, dict):
                ospec = onFillOrder.data.copy()
            else:
                ospec = onFillOrder

            if ospec:
                _data: Dict[str, Any] = getattr(self, "_data")  # type: ignore[attr-defined]
                if "Orders" not in _data:
                    _data.update({"Orders": []})

                ospec.update({"Uic": _data["Uic"]})
                ospec.update({"BuySell": direction_invert(_data["BuySell"])})
                ospec.update({"AssetType": _data["AssetType"]})
                if "Amount" not in ospec:
                    ospec.update({"Amount": _data["Amount"]})
                _data["Orders"].append(ospec)
