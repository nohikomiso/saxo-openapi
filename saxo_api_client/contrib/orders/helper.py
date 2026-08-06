from datetime import datetime
from typing import Any

import saxo_api_client.definitions.orders as OD


def direction_from_amount(Amount: int | float) -> str:
    """direction_from_amount - determine direction from the sign of the amount.

    if Amount > 0 : Buy
    if Amount < 0 : Sell
    """
    return OD.Direction.Buy if Amount > 0 else OD.Direction.Sell


def direction_invert(direction: str) -> str:
    """direction_invert - Buy  becomes Sell, Sell becomes Buy."""
    if direction not in [OD.Direction.Buy, OD.Direction.Sell]:
        raise ValueError(f"wrong value for direction: {direction}")

    return OD.Direction.Buy if direction == OD.Direction.Sell else OD.Direction.Sell


def _tie_account_recursive(
    node: dict[str, Any],
    account_key: str,
    inherited_manual: bool | None,
) -> None:
    """Propagate AccountKey and ManualOrder through nested Orders trees."""
    manual = node.get("ManualOrder", inherited_manual)
    for child in node.get("Orders") or []:
        child["AccountKey"] = account_key
        if manual is not None and "ManualOrder" not in child:
            child["ManualOrder"] = manual
        _tie_account_recursive(child, account_key, manual)


def tie_account_to_order(AccountKey: str, order: dict[str, Any] | Any) -> dict[str, Any]:
    """tie_account_to_order - inject the AccountKey in the orderbody.

    An order specification is 'anonymous'. To apply it to an account it needs
    the AccountKey of the account.

    Parameters
    ----------
    AccountKey: string (required)
        the accountkey

    order: dict representing an orderbody or <...>Order instance
        the details of the order.
    """
    _r = order.copy() if isinstance(order, dict) else order.data.copy()

    # add the key to the orderbody, but ONLY if this is not a positionclose
    # body
    if "PositionId" not in _r:
        _r.update({"AccountKey": AccountKey})

    # and add it to related orders in Orders (if any), propagating ManualOrder if set
    if "Orders" in _r:
        _tie_account_recursive(_r, AccountKey, _r.get("ManualOrder"))

    return _r


def order_duration_spec(
    OrderDurationType: str,
    allowedDT: list[str],
    GTDDate: str | datetime | None = None,
) -> dict[str, Any]:
    """order_duration_spec - create a SAXO order duration from a date.

    This function returns a dict containing the definition of the
    duration. In case of an order where the GTDDate is specified the
    definition is extended.

    Parameters
    ----------

    GTDDate: string or datetime (required if Dur.Type == GTD)
        the GTD-datetime


    Examples
    --------

    >>> duration = OD.OrderDurationType.GoodTillDate
    >>> d = order_duration_spec(duration, "2017-12-12"))
    >>> print(json.dumps(d, indent=2))
    {
      "DurationType": "GoodTillDate",
      "ExpirationDateContainsTime": true,
      "ExpirationDateTime": "2017-12-12T00:00"
    }
    # Or by using datetime ...
    >>> d = order_duration_spec(dt, datetime(2017, 12, 12))
    >>> print(json.dumps(d, indent=2))
    {
      "DurationType": "GoodTillDate",
      "ExpirationDateContainsTime": true,
      "ExpirationDateTime": "2017-12-12T00:00"
    }
    >>> duration = OD.OrderDurationType.GoodTillCancel
    >>> d = order_duration_spec(dt)
    >>> print(json.dumps(d, indent=2))
    {
      "DurationType": "GoodTillCancel"
    }

    """

    odspec: dict[str, Any] = dict({"DurationType": OrderDurationType})

    # allowed OrderDurationTypes:
    if OrderDurationType not in allowedDT:
        raise ValueError(f"OrderDurationType: {OrderDurationType} is not supported")

    if OrderDurationType == OD.OrderDurationType.GoodTillDate:
        if GTDDate is None:
            raise ValueError("Missing GTDDate")

        _gtdtime: datetime
        if isinstance(GTDDate, str):
            try:
                _gtdtime = datetime.strptime(GTDDate, "%Y-%m-%d")
            except ValueError:
                # a ValueError is raised in case of wrong format
                _gtdtime = datetime.strptime(GTDDate, "%Y-%m-%dT%H:%M")
        else:
            # After None check and isinstance check, GTDDate is guaranteed to be datetime
            _gtdtime = GTDDate

        odspec.update(
            {
                "ExpirationDateContainsTime": True,
                "ExpirationDateTime": _gtdtime.strftime("%Y-%m-%dT%H:%M"),
            }
        )

    return odspec
