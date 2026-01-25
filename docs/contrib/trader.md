# SaxoTrader Helper

`saxo_openapi.contrib.trader.SaxoTrader` は、注文発注プロセスを大幅に簡素化する高レベルヘルパークラスです。
アカウント情報の管理と注文リクエストの作成・実行を1つのクラスにカプセル化しています。

## 初期化

`API` クライアントインスタンスを渡して初期化します。`AccountKey` は初回利用時に自動的に取得されます。

```python
from saxo_openapi import API
from saxo_openapi.contrib.trader import SaxoTrader

token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)
trader = SaxoTrader(client)
```

## 注文メソッド

### 成行注文 (Market Order)

`market_order` メソッドを使用します。数量（Amount）の符号で売買方向（Buy/Sell）が自動判定されます。

```python
# EURUSD (Uic=21) を 10,000 単位購入 (Buy)
response = trader.market_order(Uic=21, Amount=10000)
print(f"OrderId: {response['OrderId']}")

# EURUSD を 10,000 単位売却 (Sell)
response = trader.market_order(Uic=21, Amount=-10000)
```

### 指値注文 (Limit Order)

「指値」に対応します。

`limit_order` メソッドを使用します。

```python
# EURUSD を 1.1025 で 10,000 単位購入
response = trader.limit_order(Uic=21, Amount=10000, OrderPrice=1.1025)
```

### 逆指値注文 (Stop Order - Smart Routing)

「逆指値 -> 成行」に対応します。

`stop_order` メソッドは**スマート注文ルーティング**をサポートしています。
銘柄がサポートする注文タイプ（`Stop` または `StopIfTraded`）を自動的に判別して適切な注文を発行します。

```python
# 損切り: 1.1000 で 10,000 単位売却
# スマートルーティング機能により、FXはStopOrder、Stock/CFDはStopIfTradedOrderに
# 自動的に変換されて発注されます。
response = trader.stop_order(Uic=21, Amount=-10000, OrderPrice=1.1000)
```

### ストップリミット注文 (Stop Limit Order)

「逆指値 -> 指値」に対応します。

CFDなどでよく使用される、逆指値でトリガーし指値を発注する注文です。

```python
# AAPL CFD (Uic=211)
# 150.0 でトリガーし、149.5 の指値で売却
response = trader.stop_limit_order(
    Uic=211,
    Amount=-1,
    OrderPrice=150.0,
    StopLimitPrice=149.5,
    AssetType="CfdOnStock"
)
```

### Stop If Traded Order

市場で取引が成立した場合にトリガーされるストップ注文です。
`stop_order` を使用した場合、銘柄がこの注文タイプしかサポートしていない（Stopが使えない）場合は、**自動的にこのタイプに切り替わります**。
もし明示的にこのタイプを指定したい場合は、以下のメソッドを使用してください。

```python
response = trader.stop_if_traded_order(
    Uic=211,
    Amount=-1,
    OrderPrice=150.0,
    AssetType="CfdOnStock"
)
```

## その他のオプション

各メソッドは `kwargs` を通じて `MarketOrder` や `LimitOrder` などの基礎となるクラスのオプションパラメータを受け入れます。

```python
# 参照IDを指定して発注
trader.market_order(
    Uic=21, 
    Amount=10000, 
    ExternalReference="AlgorithmicTrade_001"
)
```

## validate_order

Saxoの `PrecheckOrder` エンドポイントを使用して、実際に注文を発注することなく注文内容を検証します。
発注前に「市場価格と乖離している（OnWrongSideOfMarket）」などのエラーやパラメータの不備を確認するのに役立ちます。

```python
# Market Orderの検証
order_spec = MarketOrder(Uic=21, Amount=1000, AssetType="FxSpot")

# 注文は発注されず、検証結果のみが返る
result = trader.validate_order(order_spec)
print(result)
```


## 両建て (Hedging) と IsForceOpen について

SaxoTraderは、銘柄のタイプに応じて `IsForceOpen`（強制的に新規ポジションとして建てるフラグ）の扱いを自動で調整します。

- **Stock (現物株式)**: Saxo APIの仕様上、`IsForceOpen` はサポートされていません。そのため、`SaxoTrader` は現物株式の注文から自動的にこのパラメータを除外します。
- **CFD / FX**: これらの銘柄は `IsForceOpen` をサポートしています。`SaxoTrader` はパラメータを変更せずそのまま送信するため、**両建て（Hedging）が可能**です。

```python
# CFDでの両建て例 (IsForceOpen=True を指定可能)
trader.market_order(
    Uic=211, 
    Amount=10, 
    AssetType="CfdOnStock",
    IsForceOpen=True  # CFDなら有効
)
```

---

## 関連ドキュメント

- [option_trader.md](option_trader.md) - オプション取引用ヘルパー（OptionTrader & OptionFinder）
- [orders.md](orders.md) - 注文ヘルパークラス（MarketOrder, LimitOrder等）
- [Trading API](../api/trading/README.md) - Trading エンドポイント
