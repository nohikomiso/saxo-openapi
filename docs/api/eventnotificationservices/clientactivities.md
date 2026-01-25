# Client Activities Event Notification Services

このセクションでは、クライアントアクティビティのイベント通知購読およびアクティビティの取得を管理するためのエンドポイントを扱います。

---

## `CreateSubscriptionForClientEvents`

クライアントイベントをリッスンするためのアクティブな購読を設定します。

### エンドポイント

`POST openapi/ens/v1/activities/subscriptions`

### リクエストボディ (`data`)

| 名前         | タイプ   | 説明                                      |
|--------------|----------|-------------------------------------------|
| ContextId    | string   | 購読のコンテキストID。                    |
| ReferenceId  | string   | この購読の参照ID。                        |
| Events       | array of string | 購読するイベントのタイプ (例: `OrderActivities`)。|

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.eventnotificationservices as ens
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストボディのデータ
data = {
    "ContextId": "my_client_events_context",
    "ReferenceId": "my_order_activities_sub",
    "Events": ["OrderActivities"] # 購読したいイベントタイプ
}

# リクエストの作成と実行
r = ens.clientactivities.CreateSubscriptionForClientEvents(data=data)
rv = client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# レスポンスボディの表示
print(json.dumps(rv, indent=2))
```

### レスポンス例

```json
{
  "ContextId": "my_client_events_context",
  "ReferenceId": "my_order_activities_sub",
  "Snapshot": {
    "Data": []
  }
}
```

---

## `RemoveSubscription`

購読IDで識別される現在のセッションの購読を削除します。

### エンドポイント

`DELETE openapi/ens/v1/activities/subscriptions/{ContextId}/{ReferenceId}`

### パラメータ

| 名前         | 位置 | 説明                                      |
|--------------|------|-------------------------------------------|
| ContextId    | path | 購読のコンテキストID。                    |
| ReferenceId  | path | 購読の参照ID。                            |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.eventnotificationservices as ens

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 削除するContextIdとReferenceIdを指定
ContextId = "my_client_events_context"
ReferenceId = "my_order_activities_sub"

# リクエストの作成と実行
r = ens.clientactivities.RemoveSubscription(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `202 Accepted` を返しますが、レスポンスボディにデータは含まれません。

---

## `RemoveSubscriptions`

このリソースの現在のセッションの複数の/すべての購読を削除し、サーバー上のすべてのリソースを解放します。

### エンドポイント

`DELETE openapi/ens/v1/activities/subscriptions/{ContextId}`

### パラメータ

| 名前         | 位置 | 説明                                      |
|--------------|------|-------------------------------------------|
| ContextId    | path | 購読のコンテキストID。                    |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.eventnotificationservices as ens

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 削除するContextIdを指定
ContextId = "my_client_events_context"

# リクエストの作成と実行
r = ens.clientactivities.RemoveSubscriptions(ContextId=ContextId)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `202 Accepted` を返しますが、レスポンスボディにデータは含まれません。

---

## `GetActivities`

リクエストのパラメータで指定されたアクティビティのリストを返します。

### エンドポイント

`GET openapi/ens/v1/activities`

### パラメータ

| 名前         | 位置 | 説明                                      |
|--------------|------|-------------------------------------------|
| ClientKey    | query | アクティビティを取得するクライアントのキー。|
| FromDateTime | query | アクティビティを取得する開始日時 (ISO 8601形式)。|
| ToDateTime   | query | アクティビティを取得する終了日時 (ISO 8601形式)。|
| ActivityType | query | 取得するアクティビティのタイプ (例: `OrderActivities`)。|

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.eventnotificationservices as ens
import json
from datetime import datetime, timedelta

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストパラメータ
params = {
    "ClientKey": "Cf4xZ4v1q2fI5d5b7a3E7f==", # 実際のクライアントキーに置き換える
    "FromDateTime": (datetime.now() - timedelta(days=7)).isoformat(),
    "ToDateTime": datetime.now().isoformat(),
    "ActivityType": "OrderActivities"
}

# リクエストの作成と実行
r = ens.clientactivities.GetActivities(params=params)
rv = client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# レスポンスボディの表示
print(json.dumps(rv, indent=2))
```

### レスポンス例

```json
{
  "Data": [
    {
      "ActivityId": "12345",
      "ActivityType": "OrderActivities",
      "ClientKey": "Cf4xZ4v1q2fI5d5b7a3E7f==",
      "DateTime": "2025-11-16T10:00:00.000Z",
      "Description": "Order placed for AAPL",
      "Source": "TradingPlatform"
    }
  ],
  "__VIEWSTATE": "..."
}
```
