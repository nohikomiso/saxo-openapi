# NetPositions

NetPositions エンドポイントは、ネットポジション（純保有ポジション）情報を取得および管理するための機能を提供します。

## エンドポイント一覧

| クラス名 | メソッド | パス | 説明 |
|---------|----------|------|------|
| `SingleNetPosition` | GET | /openapi/port/v1/netpositions/{NetPositionId} | 指定されたIDのネットポジションを取得します。 |
| `SingleNetPositionDetails` | GET | /openapi/port/v1/netpositions/{NetPositionId}/details | 指定されたIDのネットポジションの詳細を取得します。 |
| `NetPositionsMe` | GET | /openapi/port/v1/netpositions/me | ログインユーザーのネットポジション一覧を取得します。 |
| `NetPositionsQuery` | GET | /openapi/port/v1/netpositions | 指定された条件（クライアント、アカウントなど）に基づいてネットポジション一覧を取得します。 |
| `NetPositionListSubscription` | POST | /openapi/port/v1/netpositions/subscriptions | ネットポジションのサブスクリプションを作成します。 |
| `NetPositionSubscriptionRemoveMultiple` | DELETE | /openapi/port/v1/netpositions/subscriptions/{ContextId}/ | 指定されたコンテキストの全てのサブスクリプションを削除します。 |
| `NetPositionSubscriptionRemove` | DELETE | /openapi/port/v1/positions/subscriptions/{ContextId}/{ReferenceId} | 指定されたIDのサブスクリプションを削除します。 (注意: パスが `positions` となっています) |

## 使用例

### ネットポジション取得 (SingleNetPosition)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

net_position_id = "GBPCAD__FxSpot"
params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = netpositions.SingleNetPosition(
    NetPositionId=net_position_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/netpositions/single_net_position_response.json)

### ネットポジション詳細取得 (SingleNetPositionDetails)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

net_position_id = "GBPCAD__FxSpot"
params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = netpositions.SingleNetPositionDetails(
    NetPositionId=net_position_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/netpositions/single_net_position_details_response.json)

### 自分のネットポジション一覧取得 (NetPositionsMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

r = netpositions.NetPositionsMe()
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/netpositions/net_positions_me_response.json)

### ネットポジション検索 (NetPositionsQuery)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = netpositions.NetPositionsQuery(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/netpositions/net_positions_query_response.json)

### ネットポジション・サブスクリプション作成 (NetPositionListSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions
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

r = netpositions.NetPositionListSubscription(data=data)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/netpositions/net_position_list_subscription_response.json)

### 複数サブスクリプション削除 (NetPositionSubscriptionRemoveMultiple)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
params = {
    "Tag": "MyTag"
}

r = netpositions.NetPositionSubscriptionRemoveMultiple(
    ContextId=context_id,
    params=params
)
client.request(r)

assert r.status_code == r.expected_status
```

### IDによるサブスクリプション削除 (NetPositionSubscriptionRemove)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import netpositions

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
reference_id = "Reference_Id"

r = netpositions.NetPositionSubscriptionRemove(
    ContextId=context_id,
    ReferenceId=reference_id
)
client.request(r)

assert r.status_code == r.expected_status
```
