# Closed Positions

Closed Positions エンドポイントは、クローズされたポジションの情報を取得および管理するための機能を提供します。

## エンドポイント一覧

| クラス名 | メソッド | パス | 説明 |
|---------|----------|------|------|
| `ClosedPositionList` | GET | /openapi/port/v1/closedpositions/ | クエリパラメータで指定された条件を満たすクローズ済みポジションのリストを返します。 |
| `ClosedPositionById` | GET | /openapi/port/v1/closedpositions/{ClosedPositionId} | 指定されたIDのクローズ済みポジションを取得します。 |
| `ClosedPositionDetails` | GET | /openapi/port/v1/closedpositions/{ClosedPositionId}/details/ | 指定されたIDのクローズ済みポジションの詳細情報を取得します。 |
| `ClosedPositionsMe` | GET | /openapi/port/v1/closedpositions/me | ログインユーザーのクローズ済みポジションのリストを返します。 |
| `ClosedPositionSubscription` | POST | /openapi/port/v1/closedpositions/subscriptions/ | クローズ済みポジションのサブスクリプションを作成します。 |
| `ClosedPositionSubscriptionUpdate` | PATCH | /openapi/port/v1/closedpositions/subscriptions/{ContextId}/{ReferenceId} | 既存のサブスクリプションを更新（ページサイズや表示数の変更）します。 |
| `ClosedPositionSubscriptionsRemove` | DELETE | /openapi/port/v1/closedpositions/subscriptions/{ContextId} | 指定されたコンテキストの全てのサブスクリプションを削除します。 |
| `ClosedPositionSubscriptionRemoveById` | DELETE | /openapi/port/v1/closedpositions/subscriptions/{ContextId}/{ReferenceId} | 指定されたIDのサブスクリプションを削除します。 |

## 使用例

### クローズ済みポジション一覧の取得 (ClosedPositionList)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = closedpositions.ClosedPositionList(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/closedpositions/closed_position_list_response.json)

### IDによるクローズ済みポジションの取得 (ClosedPositionById)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

closed_position_id = "212702698-212702774"
params = {
    "ClientKey": "ClientKey_Here"
}

r = closedpositions.ClosedPositionById(
    ClosedPositionId=closed_position_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/closedpositions/closed_position_by_id_response.json)

### クローズ済みポジション詳細の取得 (ClosedPositionDetails)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

closed_position_id = "212702698-212702774"
params = {
    "ClientKey": "ClientKey_Here"
}

r = closedpositions.ClosedPositionDetails(
    ClosedPositionId=closed_position_id,
    params=params
)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/closedpositions/closed_position_details_response.json)

### 自分のクローズ済みポジション一覧の取得 (ClosedPositionsMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "$top": 10
}

r = closedpositions.ClosedPositionsMe(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/closedpositions/closed_positions_me_response.json)

### サブスクリプションの作成 (ClosedPositionSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
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

r = closedpositions.ClosedPositionSubscription(data=data)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/closedpositions/closed_position_subscription_response.json)

### サブスクリプションの更新 (ClosedPositionSubscriptionUpdate)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
reference_id = "Reference_Id"

data = {
    "Arguments": {
        "$top": 20
    }
}

r = closedpositions.ClosedPositionSubscriptionUpdate(
    ContextId=context_id,
    ReferenceId=reference_id,
    data=data
)
client.request(r)

# No response data expected for 200 OK
assert r.status_code == r.expected_status
```

### サブスクリプションの削除 (ClosedPositionSubscriptionsRemove)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"

r = closedpositions.ClosedPositionSubscriptionsRemove(ContextId=context_id)
client.request(r)

assert r.status_code == r.expected_status
```

### IDによるサブスクリプションの削除 (ClosedPositionSubscriptionRemoveById)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import closedpositions

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
reference_id = "Reference_Id"

r = closedpositions.ClosedPositionSubscriptionRemoveById(
    ContextId=context_id,
    ReferenceId=reference_id
)
client.request(r)

assert r.status_code == r.expected_status
```
