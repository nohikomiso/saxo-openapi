# Orders (Portfolio)

Portfolio Orders エンドポイントは、ポートフォリオ内のオープンオーダー（未約定注文）情報を取得および管理するための機能を提供します。

## エンドポイント一覧

| クラス名 | メソッド | パス | 説明 |
|---------|----------|------|------|
| `GetOpenOrder` | GET | /openapi/port/v1/orders/{ClientKey}/{OrderId} | 指定されたクライアントと注文IDのオープンオーダーを取得します。 |
| `GetOpenOrdersMe` | GET | /openapi/port/v1/orders/me/ | ログインユーザーのオープンオーダー一覧を取得します。 |
| `OrderDetails` | GET | /openapi/port/v1/orders/{OrderId}/details/ | 指定された注文IDの詳細情報を取得します。 |
| `GetAllOpenOrders` | GET | /openapi/port/v1/orders/ | 指定されたアカウントまたはクライアントの全てのオープンオーダーを取得します。 |
| `CreateOpenOrdersSubscription` | POST | /openapi/port/v1/orders/subscriptions | オープンオーダーのサブスクリプションを作成します。 |
| `RemoveOpenOrderSubscriptionsByTag` | DELETE | /openapi/port/v1/orders/subscriptions/{ContextId}/ | 指定されたコンテキストの全てのサブスクリプションを削除します。 |
| `RemoveOpenOrderSubscription` | DELETE | /openapi/port/v1/orders/subscriptions/{ContextId}/{ReferenceId} | 指定されたIDのサブスクリプションを削除します。 |

## 使用例

### 特定のオープンオーダー取得 (GetOpenOrder)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

client_key = "ClientKey_Here"
order_id = "OrderId_Here"
params = {
    "FieldGroups": "DisplayAndFormat,ExchangeInfo"
}

r = orders.GetOpenOrder(
    ClientKey=client_key,
    OrderId=order_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/orders/get_open_order_response.json)

### 自分のオープンオーダー一覧取得 (GetOpenOrdersMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "FieldGroups": "DisplayAndFormat,ExchangeInfo"
}

r = orders.GetOpenOrdersMe(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/orders/get_open_orders_me_response.json)

### オープンオーダー詳細取得 (OrderDetails)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

order_id = "OrderId_Here"
params = {
    "FieldGroups": "DisplayAndFormat,ExchangeInfo"
}

r = orders.OrderDetails(
    OrderId=order_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/orders/order_details_response.json)

### 全てのオープンオーダー取得 (GetAllOpenOrders)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here",
    "FieldGroups": "DisplayAndFormat,ExchangeInfo"
}

r = orders.GetAllOpenOrders(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/orders/get_all_open_orders_response.json)

### オープンオーダー・サブスクリプション作成 (CreateOpenOrdersSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "Arguments": {
        "AccountKey": "AccountKey_Here",
        "ClientKey": "ClientKey_Here"
    },
    "ContextId": "Context_Id",
    "ReferenceId": "Reference_Id"
}

r = orders.CreateOpenOrdersSubscription(data=data)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/orders/create_open_orders_subscription_response.json)

### タグによるサブスクリプション削除 (RemoveOpenOrderSubscriptionsByTag)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
params = {
    "Tag": "MyTag"
}

r = orders.RemoveOpenOrderSubscriptionsByTag(
    ContextId=context_id,
    params=params
)
client.request(r)

assert r.status_code == r.expected_status
```

### IDによるサブスクリプション削除 (RemoveOpenOrderSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import orders

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
reference_id = "Reference_Id"

r = orders.RemoveOpenOrderSubscription(
    ContextId=context_id,
    ReferenceId=reference_id
)
client.request(r)

assert r.status_code == r.expected_status
```
