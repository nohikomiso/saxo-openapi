# Portfolio Positions

ポジション（建玉）データを取得・管理するためのエンドポイント群です。

## Endpoints

### SinglePosition

単一のポジションを取得します。

- **URL**: `openapi/port/v1/positions/{PositionId}`
- **Method**: `GET`

#### Request

**Parameters**

- `PositionId` (string, required): ポジションID
- `params` (dict, required): クエリパラメータ

[Query Parameters Schema](../../schemas/portfolio/positions/single_position_params.json)

#### Response

[Response Schema](../../schemas/portfolio/positions/single_position_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {"ClientKey": "ClientKey_Here"}
r = pf.positions.SinglePosition(PositionId="123456", params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### SinglePositionDetails

単一のポジションの詳細を取得します。

- **URL**: `openapi/port/v1/positions/{PositionId}/details`
- **Method**: `GET`

#### Request

**Parameters**

- `PositionId` (string, required): ポジションID
- `params` (dict, required): クエリパラメータ

[Query Parameters Schema](../../schemas/portfolio/positions/single_position_details_params.json)

#### Response

[Response Schema](../../schemas/portfolio/positions/single_position_details_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {"ClientKey": "ClientKey_Here"}
r = pf.positions.SinglePositionDetails(PositionId="123456", params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### PositionsMe

ログイン中のクライアントのポジションを取得します。

- **URL**: `openapi/port/v1/positions/me`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータはオプションです。

[Query Parameters Schema](../../schemas/portfolio/positions/positions_me_params.json)

#### Response

[Response Schema](../../schemas/portfolio/positions/positions_me_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = pf.positions.PositionsMe()
client.request(r)
print(json.dumps(r.response, indent=2))
```

### PositionsQuery

クライアント、アカウントグループ、アカウント、またはポジションを指定してポジションを取得します。

- **URL**: `openapi/port/v1/positions`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータとして辞書を渡します。

[Query Parameters Schema](../../schemas/portfolio/positions/positions_query_params.json)

#### Response

[Response Schema](../../schemas/portfolio/positions/positions_query_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {
    "ClientKey": "ClientKey_Here",
    "AccountGroupKey": "AccountGroupKey_Here"
}
r = pf.positions.PositionsQuery(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### PositionListSubscription

ポジションリストのサブスクリプション（購読）を設定し、初期スナップショットを返します。

- **URL**: `openapi/port/v1/positions/subscriptions`
- **Method**: `POST`

#### Request

**Parameters**

クエリパラメータはオプションです。

[Query Parameters Schema](../../schemas/portfolio/positions/position_list_subscription_params.json)

**Body**

リクエストボディとして辞書を渡します。

[Request Body Schema](../../schemas/portfolio/positions/position_list_subscription_body.json)

#### Response

[Response Schema](../../schemas/portfolio/positions/position_list_subscription_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
data = {
    "Arguments": {
        "ClientKey": "ClientKey_Here"
    },
    "ContextId": "explorer_12345",
    "ReferenceId": "MyPosSub"
}
r = pf.positions.PositionListSubscription(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### PositionSubscriptionPageSize

実行中のポジションサブスクリプションのページサイズ（表示されるポジション数）を拡張または縮小します。

- **URL**: `openapi/port/v1/positions/subscriptions/{ContextId}/{ReferenceId}`
- **Method**: `PATCH`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `ReferenceId` (string, required): リファレンスID
- `data` (dict, required): リクエストボディ

[Request Body Schema](../../schemas/portfolio/positions/position_subscription_page_size_body.json)

#### Response

データは返されません（202 Accepted）。

[Response Schema](../../schemas/portfolio/positions/position_subscription_page_size_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "explorer_12345"
ReferenceId = "MyPosSub"
data = {"PageSize": 50}
r = pf.positions.PositionSubscriptionPageSize(ContextId, ReferenceId, data=data)
client.request(r)
assert r.status_code == r.expected_status
```

### PositionSubscriptionRemoveMultiple

指定されたContextIdの複数のサブスクリプションを削除します。

- **URL**: `openapi/port/v1/positions/subscriptions/{ContextId}/`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `params` (dict, optional): クエリパラメータ（Tagなど）

[Query Parameters Schema](../../schemas/portfolio/positions/position_subscription_remove_multiple_params.json)

#### Response

データは返されません（202 Accepted）。

[Response Schema](../../schemas/portfolio/positions/position_subscription_remove_multiple_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "explorer_12345"
params = {"Tag": "MyTag"}
r = pf.positions.PositionSubscriptionRemoveMultiple(ContextId, params=params)
client.request(r)
assert r.status_code == r.expected_status
```

### PositionSubscriptionRemove

サブスクリプションIDで識別される現在のセッションのサブスクリプションを削除します。

- **URL**: `openapi/port/v1/positions/subscriptions/{ContextId}/{ReferenceId}`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `ReferenceId` (string, required): リファレンスID

#### Response

データは返されません（202 Accepted）。

[Response Schema](../../schemas/portfolio/positions/position_subscription_remove_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "explorer_12345"
ReferenceId = "MyPosSub"
r = pf.positions.PositionSubscriptionRemove(ContextId, ReferenceId)
client.request(r)
assert r.status_code == r.expected_status
```
