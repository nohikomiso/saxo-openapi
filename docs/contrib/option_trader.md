# OptionTrader & OptionFinder Helper

オプション取引を簡素化する高レベルヘルパークラス群です。

## 関連モジュール

- [OptionFinder](#optionfinder) - オプション契約の検索
- [OptionTrader](#optiontrader) - オプション注文の発注
- [SaxoTrader](trader.md) - FX/Stock/CFD取引用ヘルパー

---

## OptionFinder

オプション契約の検索を支援するヘルパークラスです。

### 初期化

```python
from saxo_openapi import API
from saxo_openapi.contrib.option_finder import OptionFinder

client = API(access_token="YOUR_TOKEN", environment="simulation")
finder = OptionFinder(client)
```

### オプションルート検索

キーワードでオプションルート（オプション銘柄の基盤）を検索します。

```python
roots = finder.search_option_roots("AMD")
# [OptionRoot(option_root_id=484, symbol="AMD:xcbf", ...)]

for root in roots:
    print(f"{root.symbol}: OptionRootId={root.option_root_id}")
```

### オプションチェーン取得

OptionRootId から満期日別のオプション契約一覧を取得します。

```python
chain = finder.get_option_chain(option_root_id=484)

print(f"満期日: {len(chain.expiries)} 件")
print(f"Call: {len(chain.calls)} 件, Put: {len(chain.puts)} 件")

# 個別オプションのUicを確認
for call in chain.calls[:5]:
    print(f"Strike: {call.strike_price}, Uic: {call.uic}, Expiry: {call.expiry}")
```

### 特定オプション検索

キーワード・満期日・ストライク価格から特定のオプションを一括検索します。

```python
option = finder.find_option(
    keyword="AMD",
    expiry_date="2026-06-18",
    strike_price=120.0,
    put_call="Call"
)
# OptionContract(uic=12345, strike_price=120.0, put_call="Call", ...)
```

---

## OptionTrader

オプション注文の発注を支援するヘルパークラスです。内部で `OptionFinder` を使用します。

### 初期化

```python
from saxo_openapi import API
from saxo_openapi.contrib.option_trader import OptionTrader

client = API(access_token="YOUR_TOKEN", environment="simulation")
trader = OptionTrader(client)
```

### Uic直接指定で注文

`OptionFinder` で取得したUicを直接使って注文を発注します。

```python
# コールオプション買い
response = trader.buy_option(
    uic=12345,
    amount=1,
    order_type="Limit",
    order_price=3.50,
    asset_type="StockOption"
)

# プットオプション売り
response = trader.sell_option(
    uic=67890,
    amount=1,
    order_type="Limit",
    order_price=2.00
)
```

### キーワード指定で注文（便利メソッド）

キーワードから自動でオプション検索して注文を発注します。

```python
# コールオプション買い
response = trader.buy_call(
    keyword="AMD",
    expiry_date="2026-06-18",
    strike_price=120.0,
    amount=1,
    order_type="Limit",
    order_price=5.00
)

# プットオプション売り
response = trader.sell_put(
    keyword="SPY",
    expiry_date="2026-12-18",
    strike_price=500.0,
    amount=1,
    order_price=10.00
)
```

### ポジション管理

```python
# オプション権利行使
response = trader.exercise_option(position_id="12345678")

# ポジションをクローズ（反対売買）
response = trader.close_option_position(
    uic=12345,
    amount=-1,  # 負=売り決済
    order_type="Market"
)
```

### 事前チェック

注文を発注せずに事前検証します。

```python
result = trader.validate_order(
    uic=12345,
    amount=1,
    order_type="Limit",
    order_price=3.50,
    buy_sell="Buy"
)
print(result)  # {"PreCheckResult": "Ok", ...}
```

---

## オプション戦略注文 (Multi-Leg)

複数のオプションを組み合わせた戦略注文（Straddle, Strangle, Custom等）を一括発注します。全レグが同時かつ対称的に約定すること（Atomicity）が保証されます。

### 1. 戦略テンプレート使用 (推奨)

APIが提供するデフォルト構成を使用します。

```python
from saxo_openapi.contrib.option_types import OptionsStrategyType

# Straddle戦略のデフォルト構成を取得
defaults = trader.get_strategy_defaults(
    option_root_id=484,
    strategy_type=OptionsStrategyType.STRADDLE
)

# 発注
response = trader.place_strategy_order(
    legs=defaults["Legs"],
    order_type="Limit",
    order_price=10.50
)
```

### 2. カスタム戦略構築 (上級者向け)

`create_leg` ヘルパーを使用して独自の組み合わせを作成します。

```python
# レグ1: Call買い
leg1 = trader.create_call_leg(
    keyword="AMD",
    expiry_date="2026-06-18",
    strike_price=150.0,
    action="Buy",
    to_open_close="ToOpen"
)

# レグ2: Put買い
leg2 = trader.create_put_leg(
    keyword="AMD",
    expiry_date="2026-06-18",
    strike_price=140.0,
    action="Buy",
    to_open_close="ToOpen"
)

# 一括発注 (Atomic)
response = trader.place_strategy_order(
    legs=[leg1, leg2],
    order_type="Limit",
    order_price=12.00
)
```

### 事前チェック

```python
result = trader.precheck_strategy_order(
    legs=[leg1, leg2],
    order_type="Limit",
    order_price=12.00
)
print(result) # {"PreCheckResult": "Ok", ...}
```

---

## データクラス

`saxo_openapi.contrib.option_types` で定義されています。

| クラス | 説明 |
|-------|------|
| `OptionRoot` | オプションルート（OptionRootId, Symbol, AssetType等） |
| `ExpiryInfo` | 満期日情報（Expiry, DaysToExpiry, LastTradeDate等） |
| `OptionContract` | 個別オプション契約（Uic, StrikePrice, PutCall, Expiry） |
| `OptionChain` | オプションチェーン（Calls, Puts, Expiries） |
| `OptionsStrategyType` | 戦略タイプ定数（STRADDLE, STRANGLE, VERTICAL, CUSTOM等） |

---

## 関連ドキュメント

- [orders.md](orders.md) - 注文ヘルパークラス（MarketOrder, LimitOrder等）
- [trader.md](trader.md) - SaxoTrader（FX/Stock/CFD取引用）
- [Trading API](../api/trading/README.md) - Trading エンドポイント
- [ReferenceData API](../api/referencedata/README.md) - 参照データエンドポイント
