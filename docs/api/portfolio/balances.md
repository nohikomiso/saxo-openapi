# Portfolio Balances

クライアント、アカウント、またはアカウントグループの残高データを取得するためのエンドポイント群です。

## Endpoints

### AccountBalancesMe

ログイン中のクライアントまたはアカウントの残高データを取得します。デフォルトではログイン中のクライアントが対象です。

- **URL**: `openapi/port/v1/balances/me`
- **Method**: `GET`

#### Request

パラメータは不要です。

#### Response

[Response Schema](../../schemas/portfolio/balances/account_balances_me_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = pf.balances.AccountBalancesMe()
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountBalances

クライアント、アカウントグループ、またはアカウントの残高データを取得します。

- **URL**: `openapi/port/v1/balances`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータとして辞書を渡します。

[Query Parameters Schema](../../schemas/portfolio/balances/account_balances_params.json)

#### Response

[Response Schema](../../schemas/portfolio/balances/account_balances_response.json)

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
r = pf.balances.AccountBalances(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### MarginOverview

クライアント、アカウントグループ、またはアカウントのマージン（証拠金）概要を取得します。

- **URL**: `openapi/port/v1/balances/marginoverview/`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータとして辞書を渡します。

[Query Parameters Schema](../../schemas/portfolio/balances/margin_overview_params.json)

#### Response

[Response Schema](../../schemas/portfolio/balances/margin_overview_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {
    "ClientKey": "ClientKey_Here"
}
r = pf.balances.MarginOverview(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### BalanceSubscriptionCreate

残高のサブスクリプション（購読）を設定し、初期スナップショットを返します。

- **URL**: `openapi/port/v1/balances/subscriptions`
- **Method**: `POST`

#### Request

**Body**

リクエストボディとして辞書を渡します。

[Request Body Schema](../../schemas/portfolio/balances/balance_subscription_create_body.json)

#### Response

[Response Schema](../../schemas/portfolio/balances/balance_subscription_create_response.json)

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
    "ReferenceId": "MyBalanceSub"
}
r = pf.balances.BalanceSubscriptionCreate(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### BalanceSubscriptionRemoveByTag

現在のセッションの複数のサブスクリプションを削除し、サーバー上のリソースを解放します。

- **URL**: `openapi/port/v1/balances/subscriptions/{ContextId}`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `params` (dict, required): クエリパラメータ（Tagなど）

[Query Parameters Schema](../../schemas/portfolio/balances/balance_subscription_remove_by_tag_params.json)

#### Response

データは返されません（201 Created/No Content）。

[Response Schema](../../schemas/portfolio/balances/balance_subscription_remove_by_tag_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "explorer_12345"
params = {"Tag": "MyTag"}
r = pf.balances.BalanceSubscriptionRemoveByTag(ContextId=ContextId, params=params)
client.request(r)
assert r.status_code == r.expected_status
```

### BalanceSubscriptionRemoveById

サブスクリプションIDで識別される現在のセッションのサブスクリプションを削除します。

- **URL**: `openapi/port/v1/balances/subscriptions/{ContextId}/{ReferenceId}`
- **Method**: `DELETE`

#### Request

**Parameters**

- `ContextId` (string, required): コンテキストID
- `ReferenceId` (string, required): リファレンスID

#### Response

データは返されません（201 Created/No Content）。

[Response Schema](../../schemas/portfolio/balances/balance_subscription_remove_by_id_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContextId = "explorer_12345"
ReferenceId = "MyBalanceSub"
r = pf.balances.BalanceSubscriptionRemoveById(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)
assert r.status_code == r.expected_status
```
