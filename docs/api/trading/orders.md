# Trading Orders

注文の発注、変更、キャンセル、および事前チェックを行うためのエンドポイント群です。

## Endpoints

### Order

新規注文を発注します。

- **URL**: `openapi/trade/v2/orders`
- **Method**: `POST`

#### Request

**Body**

リクエストボディとして注文詳細（辞書）を渡します。

[Request Body Schema](../../schemas/trading/orders/order_body.json)

#### Response

[Response Schema](../../schemas/trading/orders/order_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
data = {
    "Uic": 21,
    "BuySell": "Buy",
    "AssetType": "Stock",
    "Amount": 100,
    "OrderPrice": 150.5,
    "OrderType": "Limit",
    "OrderDuration": {"DurationType": "DayOrder"}
}
r = tr.orders.Order(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### ChangeOrder

既存の1つ以上の注文を変更します。

- **URL**: `openapi/trade/v2/orders`
- **Method**: `PATCH`

#### Request

**Body**

リクエストボディとして変更内容（辞書）を渡します。

[Request Body Schema](../../schemas/trading/orders/change_order_body.json)

#### Response

[Response Schema](../../schemas/trading/orders/change_order_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
data = {
    "OrderId": "12345678",
    "Amount": 200,
    "OrderPrice": 151.0
}
r = tr.orders.ChangeOrder(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### CancelOrders

1つ以上の注文をキャンセルします。

- **URL**: `openapi/trade/v2/orders/{OrderIds}`
- **Method**: `DELETE`

#### Request

**Parameters**

- `OrderIds` (string, required): カンマ区切りの注文ID文字列
- `params` (dict, required): クエリパラメータ（AccountKeyなど）

[Query Parameters Schema](../../schemas/trading/orders/cancel_orders_params.json)

#### Response

[Response Schema](../../schemas/trading/orders/cancel_orders_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
OrderIds = "12345678,87654321"
params = {"AccountKey": "AccountKey_Here"}
r = tr.orders.CancelOrders(OrderIds=OrderIds, params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### PrecheckOrder

注文の事前チェックを行います（証拠金シミュレーションなど）。

- **URL**: `openapi/trade/v2/orders/precheck`
- **Method**: `POST`

#### Request

**Body**

リクエストボディとして注文詳細（辞書）を渡します。

[Request Body Schema](../../schemas/trading/orders/precheck_order_body.json)

#### Response

[Response Schema](../../schemas/trading/orders/precheck_order_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
data = {
    "Uic": 21,
    "BuySell": "Buy",
    "AssetType": "Stock",
    "Amount": 1000,
    "OrderPrice": 150.5,
    "OrderType": "Limit",
    "OrderDuration": {"DurationType": "DayOrder"},
    "FieldGroups": ["Costs", "Margin"]
}
r = tr.orders.PrecheckOrder(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```
