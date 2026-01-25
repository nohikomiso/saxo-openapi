# Info Prices

## 概要

Info Prices（情報価格）は、金融商品の価格情報を取得するためのエンドポイント群です。単一商品・複数商品の価格取得、およびWebSocket経由での価格ストリーミング購読を管理します。

## エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| InfoPrice | GET | 単一商品の情報価格を取得 |
| InfoPrices | GET | 複数商品の情報価格リストを取得 |
| CreateInfoPriceSubscription | POST | 情報価格のWebSocket購読を作成 |
| RemoveInfoPriceSubscriptionsByTag | DELETE | タグによる情報価格購読を削除 |
| RemoveInfoPriceSubscriptionById | DELETE | IDによる情報価格購読を削除 |

## InfoPrice

指定されたパラメータを使用して、単一商品の情報価格を取得します。

### パラメータ

- **params** (dict, required): クエリパラメータ
  - Uic: 商品ID
  - AssetType: 資産タイプ
  - FieldGroups: 取得するフィールドグループ（オプション）

### JSON Schema

- **Params**: [info_price_params.json](../../schemas/trading/infoprices/info_price_params.json)
- **Response**: [info_price_response.json](../../schemas/trading/infoprices/info_price_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 単一商品の情報価格を取得
params = {
    "Uic": 211,
    "AssetType": "Stock"
}
r = tr.infoprices.InfoPrice(params=params)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## InfoPrices

複数の商品の情報価格リストを取得します。

### パラメータ

- **params** (dict, required): クエリパラメータ
  - Uics: 商品IDのリスト（カンマ区切り）
  - AssetType: 資産タイプ
  - FieldGroups: 取得するフィールドグループ（オプション）

### JSON Schema

- **Params**: [info_prices_params.json](../../schemas/trading/infoprices/info_prices_params.json)
- **Response**: [info_prices_response.json](../../schemas/trading/infoprices/info_prices_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 複数商品の情報価格リストを取得
params = {
    "Uics": "211,1533",
    "AssetType": "Stock"
}
r = tr.infoprices.InfoPrices(params=params)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## CreateInfoPriceSubscription

WebSocket経由で情報価格のリアルタイム更新を受信する購読を作成します。初回レスポンスとしてスナップショットデータが返されます。

### パラメータ

- **data** (dict, required): リクエストボディのパラメータ
  - Arguments: 購読対象のパラメータ（Uic, AssetType等）
  - ContextId: コンテキストID
  - ReferenceId: 参照ID
  - RefreshRate: 更新頻度（ミリ秒）

### JSON Schema

- **Body**: [create_info_price_subscription_body.json](../../schemas/trading/infoprices/create_info_price_subscription_body.json)
- **Response**: [create_info_price_subscription_response.json](../../schemas/trading/infoprices/create_info_price_subscription_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 情報価格購読を作成
data = {
    "Arguments": {
        "Uic": 211,
        "AssetType": "Stock"
    },
    "ContextId": "ctxt_20190316",
    "ReferenceId": "pri_01",
    "RefreshRate": 1000
}
r = tr.infoprices.CreateInfoPriceSubscription(data=data)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## RemoveInfoPriceSubscriptionsByTag

タグを指定して、1つ以上の情報価格購読を削除します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **params** (dict, optional): クエリパラメータ
  - Tag: 削除対象のタグ

### JSON Schema

- **Params**: [remove_info_price_subscriptions_by_tag_params.json](../../schemas/trading/infoprices/remove_info_price_subscriptions_by_tag_params.json)
- **Response**: [remove_info_price_subscriptions_by_tag_response.json](../../schemas/trading/infoprices/remove_info_price_subscriptions_by_tag_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# タグによる情報価格購読を削除
ContextId = "ctxt_20190316"
params = {"Tag": "MyTag"}
r = tr.infoprices.RemoveInfoPriceSubscriptionsByTag(
    ContextId=ContextId,
    params=params)
client.request(r)
assert r.status_code == r.expected_status
```

## RemoveInfoPriceSubscriptionById

単一商品の情報価格購読を削除します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **ReferenceId** (string, required): 参照ID

### JSON Schema

- **Response**: [remove_info_price_subscription_by_id_response.json](../../schemas/trading/infoprices/remove_info_price_subscription_by_id_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# IDによる情報価格購読を削除
ContextId = "ctxt_20190316"
ReferenceId = "pri_01"
r = tr.infoprices.RemoveInfoPriceSubscriptionById(
    ContextId=ContextId,
    ReferenceId=ReferenceId)
client.request(r)
assert r.status_code == r.expected_status
```

## 関連エンドポイント

- [Trading Prices](../trading/prices.md) - 取引価格エンドポイント
- [WebSocket Streaming](../../contrib/websocket.md) - WebSocketストリーミングガイド
