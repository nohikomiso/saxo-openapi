# Price Alerts Services

このセクションでは、価格アラートの定義とユーザー通知設定を管理するためのエンドポイントを扱います。

---

## `GetAllAlerts`

現在のユーザーに属するすべての価格アラート定義の未ソートリストを取得します。ユーザーが複数のアカウントを持っている場合、アラートは異なるアカウントに属している可能性があります。

### エンドポイント

`GET openapi/vas/v1/pricealerts/definitions/`

### パラメータ

| 名前  | 位置  | 説明                               |
|-------|-------|------------------------------------|
| State | query | アラートの状態 (例: `Active`, `Expired`)。 |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストパラメータ
params = {
    "State": "Active" # 取得したいアラートの状態
}

# リクエストの作成と実行
r = va.pricealerts.GetAllAlerts(params=params)
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
      "AlertDefinitionId": 30384,
      "AccountId": "Cf4xZ4v1q2fI5d5b7a3E7f==",
      "AssetType": "Stock",
      "Direction": "Up",
      "Level": 155.00,
      "Uic": 211,
      "State": "Active",
      "CreatedDate": "2025-11-20T10:00:00.000Z",
      "ExpiryDate": "2026-11-20T10:00:00.000Z"
    }
  ],
  "__VIEWSTATE": "..."
}
```

---

## `GetAlertDefinition`

現在のユーザーに対して指定された価格アラートを取得します。

### エンドポイント

`GET openapi/vas/v1/pricealerts/definitions/{AlertDefinitionId}`

### パラメータ

| 名前              | 位置 | 説明                       |
|-------------------|------|----------------------------|
| AlertDefinitionId | path | アラート定義ID。           |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# アラート定義IDを指定
AlertDefinitionId = 30384

# リクエストの作成と実行
r = va.pricealerts.GetAlertDefinition(AlertDefinitionId=AlertDefinitionId)
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
  "AlertDefinitionId": 30384,
  "AccountId": "Cf4xZ4v1q2fI5d5b7a3E7f==",
  "AssetType": "Stock",
  "Direction": "Up",
  "Level": 155.00,
  "Uic": 211,
  "State": "Active",
  "CreatedDate": "2025-11-20T10:00:00.000Z",
  "ExpiryDate": "2026-11-20T10:00:00.000Z"
}
```

---

## `CreatePriceAlert`

新しい価格アラート定義を作成します。作成された定義は、価格アラート定義IDを含むいくつかのプロパティとともに返されます。

### エンドポイント

`POST openapi/vas/v1/pricealerts/definitions/`

### リクエストボディ (`data`)

| 名前      | タイプ   | 説明                                      |
|-----------|----------|-------------------------------------------|
| AccountId | string   | アラートを関連付けるアカウントID。        |
| AssetType | string   | アラート対象の資産の種類。                |
| Direction | string   | 価格変動の方向 (`Up`, `Down`)。            |
| Level     | number   | アラートがトリガーされる価格レベル。      |
| Uic       | integer  | アラート対象の銘柄のUic。                 |
| ExpiryDate | string  | アラートの有効期限 (ISO 8601形式)。       |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json
from datetime import datetime, timedelta

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストボディのデータ
data = {
    "AccountId": "Cf4xZ4v1q2fI5d5b7a3E7f==",
    "AssetType": "Stock",
    "Direction": "Up",
    "Level": 155.00,
    "Uic": 211,
    "ExpiryDate": (datetime.now() + timedelta(days=365)).isoformat()
}

# リクエストの作成と実行
r = va.pricealerts.CreatePriceAlert(data=data)
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
  "AlertDefinitionId": 30384,
  "AccountId": "Cf4xZ4v1q2fI5d5b7a3E7f==",
  "AssetType": "Stock",
  "Direction": "Up",
  "Level": 155.00,
  "Uic": 211,
  "State": "Active",
  "CreatedDate": "2025-11-20T10:00:00.000Z",
  "ExpiryDate": "2026-11-20T10:00:00.000Z"
}
```

---

## `UpdatePriceAlert`

現在のユーザーの価格アラート定義を更新します。

### エンドポイント

`PUT openapi/vas/v1/pricealerts/definitions/{AlertDefinitionId}`

### パラメータ

| 名前              | 位置 | 説明                       |
|-------------------|------|----------------------------|
| AlertDefinitionId | path | 更新するアラート定義ID。   |

### リクエストボディ (`data`)

| 名前      | タイプ   | 説明                                      |
|-----------|----------|-------------------------------------------|
| Direction | string   | 価格変動の方向 (`Up`, `Down`)。            |
| Level     | number   | アラートがトリガーされる新しい価格レベル。 |
| ExpiryDate | string  | アラートの新しい有効期限 (ISO 8601形式)。 |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json
from datetime import datetime, timedelta

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 更新するアラート定義ID
AlertDefinitionId = 30384

# リクエストボディのデータ
data = {
    "Direction": "Down",
    "Level": 145.00,
    "ExpiryDate": (datetime.now() + timedelta(days=300)).isoformat()
}

# リクエストの作成と実行
r = va.pricealerts.UpdatePriceAlert(AlertDefinitionId=AlertDefinitionId, data=data)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `204 No Content` を返しますが、レスポンスボディにデータは含まれません。

---

## `DeletePriceAlert`

指定された価格アラート定義を削除します。アラートは現在のユーザーに属している必要があります。

### エンドポイント

`DELETE openapi/vas/v1/pricealerts/definitions/{AlertDefinitionIds}`

### パラメータ

| 名前                | 位置 | 説明                                       |
|---------------------|------|--------------------------------------------|
| AlertDefinitionIds  | path | コンマ区切りのアラート定義ID文字列。      |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 削除するアラート定義IDを指定 (複数指定可能)
AlertDefinitionIds = '30384,30386'

# リクエストの作成と実行
r = va.pricealerts.DeletePriceAlert(AlertDefinitionIds=AlertDefinitionIds)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `204 No Content` を返しますが、レスポンスボディにデータは含まれません。

---

## `GetUserNotificationSettings`

現在のユーザーの価格アラート通知設定を取得します。

### エンドポイント

`GET openapi/vas/v1/pricealerts/usersettings/`

### パラメータ
このエンドポイントはパラメータを必要としません。

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストの作成と実行
r = va.pricealerts.GetUserNotificationSettings()
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
  "AllowNotifications": True,
  "NotificationMethod": "Email",
  "EmailAddress": "user@example.com",
  "SmsNumber": null
}
```

---

## `ModifyUserNotificationSettings`

現在のユーザーの価格アラート通知設定を変更します。

### エンドポイント

`PUT openapi/vas/v1/pricealerts/usersettings/`

### リクエストボディ (`data`)

| 名前               | タイプ   | 説明                                      |
|--------------------|----------|-------------------------------------------|
| AllowNotifications | boolean  | 通知を許可するかどうか。                  |
| NotificationMethod | string   | 通知方法 (`Email`, `Sms`, `None`)。       |
| EmailAddress       | string   | 通知用のメールアドレス。                  |
| SmsNumber          | string   | 通知用のSMS番号。                         |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.valueadd as va
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストボディのデータ
data = {
    "AllowNotifications": True,
    "NotificationMethod": "Sms",
    "SmsNumber": "+1234567890"
}

# リクエストの作成と実行
r = va.pricealerts.ModifyUserNotificationSettings(data=data)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `204 No Content` を返しますが、レスポンスボディにデータは含まれません。
