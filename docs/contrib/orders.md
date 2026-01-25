# Contrib Orders

`saxo_openapi.contrib.orders` モジュールは、注文リクエストの作成を簡素化するためのヘルパークラスと関数を提供します。
これらのクラスを使用することで、複雑な辞書構造を手動で構築する代わりに、オブジェクト指向のアプローチで注文パラメータを指定できます。

## 概要

このモジュールは以下の主要なコンポーネントを提供します：

*   **注文クラス**: `MarketOrder`, `LimitOrder`, `StopOrder` など、一般的な注文タイプごとのクラス。
*   **資産クラス別サブクラス**: `MarketOrderFxSpot`, `LimitOrderStock` など、特定の資産クラスに特化したサブクラス。
*   **OnFill ヘルパー**: `TakeProfitDetails`, `StopLossDetails` など、注文約定後の関連注文（OCO注文）を指定するためのクラス。
*   **ユーティリティ関数**: `tie_account_to_order` など、注文作成を支援する関数。

## インポート

```python
from saxo_openapi.contrib.orders import (
    MarketOrder,
    LimitOrder,
    StopOrder,
    MarketCloseOrder,
    tie_account_to_order,
    TakeProfitDetails,
    StopLossDetails
)
import saxo_openapi.definitions.orders as OD
```

## 注文クラス

すべての注文クラスは `BaseOrder` を継承しており、`data` プロパティを通じて API リクエストに必要な JSON ボディ（辞書）を提供します。

### MarketOrder (成行注文)

成行注文を作成します。

```python
# EURUSD (Uic=21) を 10,000 単位購入
mo = MarketOrder(
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=10000
)
```

**資産クラス別ショートカット:**
*   `MarketOrderFxSpot(Uic, Amount, ...)`
*   `MarketOrderStock(Uic, Amount, ...)`
*   `MarketOrderCfdOnStock(Uic, Amount, ...)`

### LimitOrder (指値注文)

指値注文を作成します。

```python
# EURUSD を 1.1025 で 10,000 単位購入
lo = LimitOrder(
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=10000,
    OrderPrice=1.1025
)
```

**資産クラス別ショートカット:**
*   `LimitOrderFxSpot`
*   `LimitOrderStock`

### StopOrder (逆指値注文)

逆指値（ストップ）注文を作成します。

```python
# EURUSD が 1.1000 に達したら 10,000 単位売却（損切りなど）
so = StopOrder(
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=-10000,
    OrderPrice=1.1000
)
```

**資産クラス別ショートカット:**
*   `StopOrderFxSpot`

### StopLimitOrder (ストップリミット注文)

ストップ価格に達した後に指値注文を発注します。

```python
slo = StopLimitOrder(
    Uic=211, # AAPL CFD
    AssetType=OD.AssetType.CfdOnStock,
    Amount=1,
    OrderPrice=150.0,    # トリガー価格
    StopLimitPrice=149.5 # 指値価格
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
    OrderPrice=150.0
)
```

**資産クラス別ショートカット:**
*   `StopIfTradedOrderCfdOnStock`

### MarketCloseOrder (ポジション決済)

明示的にPositionIdを指定してポジションを決済（クローズ）します。
「Explicit Close」モード（トップレベルのPositionId指定＋入れ子の注文リスト）の複雑なJSON構造を自動的に構築します。

**使用すべきケース**:
以下のいずれかの場合に、このクラスを使用して明示的クローズ（Explicit Close）を行う必要があります。

1.  **アカウント設定が「日次ネッティング (EndOfDay)」の場合**: 日中はポジションが個別に保持されるため、特定のポジションを閉じるには `PositionId` の指定が必須です。
2.  **ポジションが「両建て (Hedging)」モードで作られた場合**: `IsForceOpen=True` で作成されたポジションは、反対売買を行っても相殺されず、**両建て（新規ポジション）**となります。そのため、このポジションを決済するには、単なる反対注文ではなく、PositionIdを指定した明示的なクローズ注文が必要です。

**注意**: アカウントが「リアルタイムネッティング (RealTime)」で、かつポジションも単純なネッティング対象（`IsForceOpen=False`）であれば、**このクラスは不要**です。通常の `MarketOrder` で反対売買を行えば、自動的に相殺決済されます。

```python
# PositionId="12345" を決済
# FxSpot USDJPY 1,000通貨を決済（ロングの決済ならSell、ショートならBuy）
mco = MarketCloseOrder(
    PositionId="12345",
    Uic=21,
    AssetType=OD.AssetType.FxSpot,
    Amount=1000,
    BuySell="Sell" # オプション（Amountの符号から推論可能だが明示指定推奨）
)
```


## 関連注文 (OnFill Orders)

注文約定時に自動的に発注される利食い（Take Profit）や損切り（Stop Loss）注文を指定できます。

```python
# 新規注文に利食いと損切りを付与
ordr = MarketOrderFxSpot(
    Uic=21,
    Amount=10000,
    TakeProfitOnFill=TakeProfitDetails(price=1.14),
    StopLossOnFill=StopLossDetails(price=1.12)
)
```

### TakeProfitDetails
利食い注文の詳細を指定します。

### StopLossDetails
損切り注文の詳細を指定します。

## ユーティリティ関数

### tie_account_to_order

注文ボディに `AccountKey` を注入します。API リクエストには通常 `AccountKey` が必要です。

```python
# アカウントキーを注文に紐付け
order_with_account = tie_account_to_order(
    AccountKey="YOUR_ACCOUNT_KEY",
    order=mo
)
```

### direction_from_amount

数量の符号から売買方向（Buy/Sell）を判定します。
*   正の値 (> 0): Buy
*   負の値 (< 0): Sell

## 完全な使用例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.orders import (
    tie_account_to_order,
    MarketOrderFxSpot,
    TakeProfitDetails,
    StopLossDetails
)

# クライアント初期化（トークンが必要）
client = API(access_token="YOUR_ACCESS_TOKEN")
AccountKey = "YOUR_ACCOUNT_KEY"

# 注文作成: EURUSD 買い, TP=1.14, SL=1.12
order_spec = MarketOrderFxSpot(
    Uic=21,
    Amount=10000,
    TakeProfitOnFill=TakeProfitDetails(price=1.14),
    StopLossOnFill=StopLossDetails(price=1.12)
)

# アカウント紐付け
order_spec = tie_account_to_order(AccountKey, order_spec)

# リクエスト作成と送信
r = tr.orders.Order(data=order_spec)
rv = client.request(r)

print(json.dumps(rv, indent=2))
```

---

## 関連ドキュメント

- [trader.md](trader.md) - SaxoTrader ヘルパー（FX/Stock/CFD取引の高レベルAPI）
- [option_trader.md](option_trader.md) - オプション取引用ヘルパー（OptionTrader & OptionFinder）
- [Trading API](../api/trading/README.md) - Trading エンドポイント
