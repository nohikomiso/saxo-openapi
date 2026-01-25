# Users (Portfolio)

Portfolio Users エンドポイントは、ユーザー情報を取得および管理するための機能を提供します。

## エンドポイント一覧

| クラス名 | メソッド | パス | 説明 |
|---------|----------|------|------|
| `UsersMe` | GET | /openapi/port/v1/users/me | ログインユーザーの詳細情報を取得します。 |
| `Users` | GET | /openapi/port/v1/users | 特定のオーナー配下の全ユーザー一覧を取得します。 |
| `UserDetails` | GET | /openapi/port/v1/users/{UserKey} | 指定されたユーザーキーのユーザー詳細情報を取得します。 |
| `UserUpdate` | PATCH | /openapi/port/v1/users/me | ログインユーザーの言語、カルチャ、タイムゾーン設定を更新します。 |

## 使用例

### 自分のユーザー情報取得 (UsersMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import users
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

r = users.UsersMe()
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/users/users_me_response.json)

### ユーザー一覧取得 (Users)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import users
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = users.Users(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/users/users_response.json)

### ユーザー詳細取得 (UserDetails)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import users
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

user_key = "UserKey_Here"

r = users.UserDetails(UserKey=user_key)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/users/user_details_response.json)

### ユーザー設定更新 (UserUpdate)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import users

client = API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "Language": "ja",
    "Culture": "ja-JP",
    "TimeZone": "Asia/Tokyo"
}

r = users.UserUpdate(data=data)
client.request(r)

assert r.status_code == r.expected_status
```
