# Contrib Orders

`saxo_api_client.contrib.orders` モジュールは、注文リクエストの作成を簡素化するためのヘルパークラスと関数を提供します。

## 目的決定表（必須）

同じ「指値・逆指値」でも **新規** と **決済** で JSON が違う。意図でクラスを選ぶ。

| 目的 | クラス.メソッド | 必須 | 禁止 |
|------|-----------------|------|------|
| 新規・成行 | `PositionOpen.market` | `is_force_open` | `PositionClose` / `PositionId` |
| 新規・指値 | `PositionOpen.limit` | + `order_price`, `is_force_open` | 同上 |
| 新規・逆指値 | `PositionOpen.stop` | + `order_price`, `is_force_open` | 同上 |
| 新規・逆指値指値 | `PositionOpen.stop_limit` | + `stop_limit_price`, `is_force_open` | 同上 |
| FIFO 決済・成行 | `PositionClose.fifo_market` | 反対方向の `buy_sell` | `PositionId` / FO=True |
| FIFO 決済・指値 | `PositionClose.fifo_limit` | + `order_price` | `PositionId` |
| FIFO 決済・逆指値 | `PositionClose.fifo_stop` | + `order_price` | standalone `StopOrder` で「閉じたつもり」 |
| FO 決済・成行 | `PositionClose.force_open_market` | **`position_id`** | standalone Market/Stop |
| FO 決済・指値 | `PositionClose.force_open_limit` | **`position_id`**, `order_price` | standalone `LimitOrder` |
| FO 決済・逆指値 | `PositionClose.force_open_stop` | **`position_id`**, `order_price` | standalone `StopOrder` |
| FO 残骸一掃 | `PositionClose.clear_force_open_market` | `ClearForceOpen` 成行 | 部分反対の積み重ね |

エージェント手順:

1. **資産タイプ** → Option なら `OptionTrader` + `ToOpen`/`ToClose`（この表は FX/Stock/CFD のみ）
2. 新規か決済か → `PositionOpen` / `PositionClose`
3. 決済なら FIFO か ForceOpen か → `fifo_*` / `force_open_*`
4. 成行 / 指値 / 逆指値か → `market` / `limit` / `stop`
5. FO 決済なら `SaxoClient.iter_open_positions` で `position_id` を取る
6. FO **部分**決済後は必ず `resolve_force_open_close_target`（stale id 禁止）。安定検証は FO×2 全量 close

## インポート

```python
from saxo_api_client.contrib.orders import (
    PositionOpen,
    PositionClose,
    MarketOrder,  # low-level; prefer PositionOpen
    LimitOrder,
    StopOrder,
    tie_account_to_order,
)
import saxo_api_client.definitions.orders as OD
```

**BREAKING:** `MarketCloseOrder` は削除済み。代わりに `PositionClose.force_open_*` を使う。

## PositionOpen（新規専用）

```python
# ForceOpen 両建てで新規ロング成行
po = PositionOpen.market(
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Buy",
    is_force_open=True,  # 必須（省略不可）
)

# 新規逆指値（これは決済ではない）
po = PositionOpen.stop(
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Buy",
    order_price=150.0,
    is_force_open=False,
)
```

## PositionClose（決済専用）

### FIFO / ネット相殺

`PositionId` なし。`IsForceOpen=False`。

```python
# ロングを成行で相殺
pc = PositionClose.fifo_market(
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Sell",
)
```

### ForceOpen 明示クローズ

`PositionId` + `Orders[]` 入れ子のみが真の FO 決済。

```python
# BAD: standalone Stop（実際は新規ショート）
# StopOrder(Uic=42, Amount=-10000, OrderPrice=entry, IsForceOpen=False)

# GOOD
pc = PositionClose.force_open_stop(
    position_id="12345",
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Sell",
    order_price=150.25,
)
```

成行 FO クローズ:

```python
pc = PositionClose.force_open_market(
    position_id="12345",
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Sell",
)
```

### ClearForceOpen

```python
pc = PositionClose.clear_force_open_market(
    uic=42,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Sell",
)
```

## 低レベル注文クラス

`MarketOrder` / `LimitOrder` / `StopOrder` 等は残置（低レベル）。推奨は `PositionOpen` / `PositionClose`。
docstring 先頭に「決済禁止」と明記済み。

### MarketOrder (成行注文)

```python
mo = MarketOrder(
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=10000,
    IsForceOpen=False,
)
```

**資産クラス別ショートカット:**
*   `MarketOrderFxSpot(Uic, Amount, ...)`
*   `MarketOrderStock(Uic, Amount, ...)`
*   `MarketOrderCfdOnStock(Uic, Amount, ...)`

### LimitOrder (指値注文)

```python
lo = LimitOrder(
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=10000,
    OrderPrice=1.1025,
    IsForceOpen=False,
)
```

**資産クラス別ショートカット:**
*   `LimitOrderFxSpot`
*   `LimitOrderStock`

### StopOrder (逆指値注文)

```python
so = StopOrder(
    Uic=211,
    AssetType=OD.AssetType.CfdOnStock,
    Amount=-1,
    OrderPrice=150.0,
    IsForceOpen=False,
)
```

**資産クラス別ショートカット:**
*   `StopOrderFxSpot`

### StopLimitOrder

```python
slo = StopLimitOrder(
    Uic=211,
    AssetType=OD.AssetType.CfdOnStock,
    Amount=-1,
    OrderPrice=150.0,
    StopLimitPrice=149.5,
    IsForceOpen=False,
)
```

**資産クラス別ショートカット:**
*   `StopLimitOrderCfdOnStock`

### StopIfTradedOrder

市場で取引が発生した場合にのみトリガーされるストップ注文です。

```python
sito = StopIfTradedOrder(
    Uic=211,
    AssetType=OD.AssetType.CfdOnStock,
    Amount=1,
    OrderPrice=150.0,
    IsForceOpen=False,
)
```

**資産クラス別ショートカット:**
*   `StopIfTradedOrderCfdOnStock`

## 関連注文 (OnFill Orders)

```python
from saxo_api_client.contrib.orders import TakeProfitDetails, StopLossDetails

ordr = PositionOpen.market(
    uic=21,
    amount=10000,
    asset_type=OD.AssetType.FxSpot,
    buy_sell="Buy",
    is_force_open=False,
    take_profit_on_fill=TakeProfitDetails(price=1.14),
    stop_loss_on_fill=StopLossDetails(price=1.12),
)
```

## ユーティリティ関数

### tie_account_to_order

注文ボディに `AccountKey` を注入します。`PositionId` + `Orders[]` の場合は入れ子側に注入します。

```python
order_with_account = tie_account_to_order(AccountKey="YOUR_ACCOUNT_KEY", order=pc)
```

### direction_from_amount

*   正の値 (> 0): Buy
*   負の値 (< 0): Sell
