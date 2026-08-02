# SaxoClient Helper

`saxo_api_client.contrib.client.SaxoClient` は、FX / Stock / CFD 向けの **Layer 3 ファサード**です。
`AccountKey` 注入・UIC 解決・注文実行／precheck を 1 クラスにまとめます。

> 旧 `SaxoTrader`（`contrib.trader`）は削除済みです。互換 shim はありません。本ドキュメントを正とします。
>
> **Options は別ルート:** `StockOption` / `StockIndexOption` / `FuturesOption` / `CfdIndexOption` は
> [`OptionTrader`](option_trader.md) + `ToOpenClose` を使う。`open_*` / `close_*` に渡すと `ValueError`。

## 初期化

`access_token` または `SaxoAuthClient` を渡します。`AccountKey` は初回利用時に自動取得されます。

```python
from saxo_api_client.contrib.client import SaxoClient

# Simulation (default when only access_token is given)
client = SaxoClient(access_token="YOUR_SIM_ACCESS_TOKEN")

# Live — pass environment explicitly OR use auth_client / from_token_file
client = SaxoClient(access_token="YOUR_LIVE_ACCESS_TOKEN", environment="live")

# Recommended for OAuth token JSON files (infers live from saxo_token_live_*.json)
client = SaxoClient.from_token_file("saxo_token_live_live.json")

# auth_client infers LIVE/SIM from app_config automatically
client = SaxoClient(auth_client=SaxoAuthClient(app_config="app_config_live.json"))
print(client.account_key)
```

> **401 on `gateway.saxobank.com/sim/...` with a Live token?**  
> You initialized with `access_token` only — the default gateway is **simulation**.  
> Use `environment="live"`, `from_token_file`, or `auth_client`.

## 推奨: 意図別 open / close

新規と決済はメソッド名で分離する（`is_force_open` / `position_id` を推測させない）。

```python
# 新規（両建て）
client.open_market(
    asset_type="FxSpot", uic=42, amount=10000, buy_sell="Buy", is_force_open=True,
)

# FO 建玉一覧（position_id はトップレベル正規化）
rows = client.iter_open_positions(uic=42)
pid = rows[0]["position_id"]

# FO 明示成行クローズ
client.close_force_open_market(
    position_id=pid, asset_type="FxSpot", uic=42, amount=10000, buy_sell="Sell",
)

# FO 部分決済後は PositionId を再解決（stale id → OrderRelatedPositionIsClosed）
target = client.resolve_force_open_close_target(previous_position_id=pid, uic=42)
if target:
    client.close_force_open_market(
        position_id=target["position_id"],
        asset_type="FxSpot",
        uic=42,
        amount=abs(target["amount"]),
        buy_sell="Sell" if target["amount"] > 0 else "Buy",
    )

# FO 明示逆指値クローズ（含み益側のみ）
client.close_force_open_stop(
    position_id=pid, asset_type="FxSpot", uic=42, amount=10000,
    buy_sell="Sell", order_price=150.25,
)

# FIFO 相殺
client.close_fifo_market(
    asset_type="FxSpot", uic=42, amount=10000, buy_sell="Sell",
)

# FO 残骸一掃
client.flatten_force_open(asset_type="FxSpot", uic=42)
```

| メソッド | 用途 |
|----------|------|
| `open_market` / `open_limit` / `open_stop` / `open_stop_limit` | 新規（`is_force_open` 必須） |
| `close_fifo_market` / `close_fifo_limit` / `close_fifo_stop` | FIFO 決済 |
| `close_force_open_market` / `close_force_open_limit` / `close_force_open_stop` | FO 明示決済 |
| `resolve_force_open_close_target` | 部分決済後の残 FO / RelatedPositionId 再解決 |
| `reduce_force_open_leg` | 部分 → 再解決 → 残量 close を 1 本化 |
| `flatten_force_open` | ClearForceOpen 一掃 |
| `iter_open_positions` | PositionId / RelatedPositionId / Status 正規化一覧 |

曖昧な `close_position()` は提供しない。

**FO 部分決済の注意:** 部分 close 後に同じ `position_id` を再利用しない。日内ネッティングで id が消える／`RelatedPositionId` に移る場合がある。組成検証は **FO×2 全量 close**（片足全量）が安定。

## Account netting（要約のみ・ルート非選択）

口座の `PositionNettingMode` / `ForceOpenDefaultValue` は **GUI・省略時のデフォルトと、決済後の見え方（EOD ゾンビ）** の文脈です。決済 API の自動選択には使いません。

```python
summary = client.summarize_client_netting()
# position_netting_mode, force_open_default_value, notes[], raw
for note in summary["notes"]:
    print(note)
```

| フィールド | 意味 |
|------------|------|
| `position_netting_mode` | 例: `EndOfDay` / Intraday 系 |
| `force_open_default_value` | 省略時の FO 寄りデフォルト |
| `notes` | Agent / preflight 向け固定 WARN |
| `raw` | `get_client_details` の生 dict |

発注経路の正本は意図別メソッド（上表）と建玉の `IsForceOpen` / AssetType。

## レガシー注文メソッド

数量（`amount`）の符号で売買方向が決まります（正=Buy、負=Sell）。FO クローズには使わない。

### 成行 (Market)

```python
response = client.market_order(asset_type="FxSpot", uic=21, amount=10000, IsForceOpen=False)
```

### 指値 (Limit)

```python
response = client.limit_order(
    asset_type="FxSpot",
    uic=21,
    amount=10000,
    order_price=1.1025,
    IsForceOpen=False,
)
```

### 逆指値 (Stop) — スマートルーティング

銘柄の `SupportedOrderTypes` に応じて `Stop` / `StopIfTraded` を選択します。

```python
response = client.stop_order(
    asset_type="FxSpot",
    uic=21,
    amount=-10000,
    order_price=1.1000,
    IsForceOpen=False,
)
```

### ストップリミット (StopLimit)

```python
response = client.stop_limit_order(
    asset_type="CfdOnStock",
    uic=211,
    amount=-1,
    order_price=150.0,
    stop_limit_price=149.5,
    IsForceOpen=False,
)
```

### 事前チェック (validate_order)

```python
from saxo_api_client.contrib.orders import PositionClose

spec = PositionClose.force_open_market(
    position_id="12345",
    uic=42,
    amount=10000,
    asset_type="FxSpot",
    buy_sell="Sell",
)
result = client.validate_order(spec)
print(result.get("PreCheckResult"))
```

## IsForceOpen

- **Stock**: API 非対応のため、`SaxoClient` が送信前に自動除去します。
- **CFD / FX**: `IsForceOpen=True` で両建て可能です。決済は `close_force_open_*`。

## 関連

- [option_trader.md](option_trader.md) — オプション取引用 Layer 3
- [orders.md](orders.md) — Layer 2 注文ビルダー（PositionOpen / PositionClose）
