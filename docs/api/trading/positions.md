# Trading Positions

## 概要

Trading Positions（取引ポジション）は、ポジションの作成・更新・行使を行うエンドポイント群です。クォートによるポジション作成、FXオプションのエクササイズメソッド更新、先物オプション・株式オプションの強制行使などを管理します。

## エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| PositionByQuote | POST | クォートを受け入れて新しいポジションを作成 |
| UpdatePosition | PATCH | 既存ポジションのプロパティを更新 |
| ExercisePosition | PUT | 特定ポジションの行使を強制 |
| ExerciseAmount | PUT | 指定UICの全ポジション横断で行使 |

## PositionByQuote

クォートを受け入れて新しいポジションを作成します。クォートは最新であり、取引可能（`Quote.PriceType=PriceType.Tradable`）である必要があります。

### パラメータ

- **data** (dict, required): リクエストボディのパラメータ
  - QuoteId: クォートID
  - Amount: 取引数量

### JSON Schema

- **Body**: [position_by_quote_body.json](../../schemas/trading/positions/position_by_quote_body.json)
- **Response**: [position_by_quote_response.json](../../schemas/trading/positions/position_by_quote_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# クォートでポジションを作成
data = {
    "QuoteId": "QUOTE_ID_HERE",
    "Amount": 1000
}
r = tr.positions.PositionByQuote(data=data)
rv = client.request(r)
print(json.dumps(rv, indent=2))
```

## UpdatePosition

既存ポジションのプロパティを更新します。これはFXオプションでエクササイズメソッドを更新する場合にのみ関連します。

### パラメータ

- **PositionId** (string, required): ポジションID
- **data** (dict, required): 更新するプロパティ

### JSON Schema

- **Body**: [update_position_body.json](../../schemas/trading/positions/update_position_body.json)
- **Response**: [update_position_response.json](../../schemas/trading/positions/update_position_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# ポジションを更新
PositionId = "1019942425"
data = {
    "ExerciseMethod": "Automatic"
}
r = tr.positions.UpdatePosition(PositionId, data=data)
rv = client.request(r)
print(json.dumps(rv, indent=2))
```

## ExercisePosition

ポジションの行使を強制します。これは先物オプション、株式オプション、株価指数オプションに関連します。

### パラメータ

- **PositionId** (string, required): ポジションID
- **data** (dict, required): 行使パラメータ

### JSON Schema

- **Body**: [exercise_position_body.json](../../schemas/trading/positions/exercise_position_body.json)
- **Response**: [exercise_position_response.json](../../schemas/trading/positions/exercise_position_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# ポジションを行使
PositionId = "1019942425"
data = {
    "Amount": 10
}
r = tr.positions.ExercisePosition(PositionId, data=data)
rv =  client.request(r)
print(json.dumps(rv, indent=2))
```

## ExerciseAmount

指定されたUICの全ポジション横断で、一定量の行使を強制します。これは先物オプション、株式オプション、株価指数オプションに関連します。

### パラメータ

- **data** (dict, required): 行使パラメータ
  - Uic: 商品ID
  - AssetType: 資産タイプ
  - Amount: 行使数量

### JSON Schema

- **Body**: [exercise_amount_body.json](../../schemas/trading/positions/exercise_amount_body.json)
- **Response**: [exercise_amount_response.json](../../schemas/trading/positions/exercise_amount_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# UIC横断で行使
data = {
    "Uic": 211,
    "AssetType": "StockOption",
    "Amount": 10
}
r = tr.positions.ExerciseAmount(data=data)
rv = client.request(r)
print(json.dumps(rv, indent=2))
```

## 関連エンドポイント

- [Portfolio Positions](../portfolio/positions.md) - ポジション情報の取得
- [Trading Orders](../trading/orders.md) - 注文管理
