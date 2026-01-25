# Trading Prices

価格のサブスクリプション、証拠金インパクトの要求、およびサブスクリプションの削除を行うためのエンドポイント群です。

## Endpoints

### CreatePriceSubscription

価格のサブスクリプションを設定し、最新価格の初期スナップショットを返します。

- **URL**: `openapi/trade/v1/prices/subscriptions`
- **Method**: `POST`

#### Request

**Body**

リクエストボディとしてサブスクリプション詳細（辞書）を渡します。

[Request Body Schema](../../schemas/trading/prices/create_price_subscription_body.json)

#### Response

[Response Schema](../../schemas/trading/prices/create_price_subscription_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
data = {
    "Arguments": {
        "Uic": 21,
        "AssetType": "Stock"
    },
    "ContextId": "Context_2023",
    "ReferenceId": "Ref_Stock_21"
}
r = tr.prices.CreatePriceSubscription(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### MarginImpactRequest

次の価格更新のいずれかで証拠金インパクトを含めるように要求します。

- **URL**: `openapi/trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}`
- **Method**: `PUT`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `ReferenceId` (string, required): リファレンスID

#### Response

データは返されません（Status Code 204）。

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "Context_2023"
ReferenceId = "Ref_Stock_21"
r = tr.prices.MarginImpactRequest(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)
print(r.status_code)
```

### PriceSubscriptionRemoveByTag

指定されたContextIdに関連する複数のサブスクリプションを削除します。オプションでタグ指定も可能です。

- **URL**: `openapi/trade/v1/prices/subscriptions/{ContextId}/`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `params` (dict, optional): クエリパラメータ（Tagなど）

[Query Parameters Schema](../../schemas/trading/prices/price_subscription_remove_by_tag_params.json)

#### Response

データは返されません（Status Code 202）。

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "Context_2023"
params = {"Tag": "MyTag"}
r = tr.prices.PriceSubscriptionRemoveByTag(ContextId=ContextId, params=params)
client.request(r)
print(r.status_code)
```

### PriceSubscriptionRemove

指定されたサブスクリプションID（ReferenceId）で識別される現在のセッションのサブスクリプションを削除します。

- **URL**: `openapi/trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `ReferenceId` (string, required): リファレンスID

#### Response

データは返されません（Status Code 202）。

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "Context_2023"
ReferenceId = "Ref_Stock_21"
r = tr.prices.PriceSubscriptionRemove(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)
print(r.status_code)
```
