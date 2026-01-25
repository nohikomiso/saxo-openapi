# Accounts

ポートフォリオのアカウントを管理するエンドポイント。

## エンドポイント

### AccountDetails

単一のアカウントの詳細を取得します。

- **URL**: `openapi/port/v1/accounts/{AccountKey}`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| AccountKey | string | 必須 | アカウントキー |

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/account_details_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
AccountKey = "..."
r = pf.accounts.AccountDetails(AccountKey=AccountKey)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountsMe

ログインユーザーが所属する特定のクライアント配下のすべてのアカウントを取得します。

- **URL**: `openapi/port/v1/accounts/me`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 任意 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accounts/accounts_me_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/accounts_me_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {}
r = pf.accounts.AccountsMe(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountListByClient

指定されたクライアントが所有するすべてのアカウントを取得します。

- **URL**: `openapi/port/v1/accounts/`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 必須 | ClientKeyを含むクエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accounts/account_list_by_client_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/account_list_by_client_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {"ClientKey": "..."}
r = pf.accounts.AccountListByClient(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountUpdate

アカウントの詳細（特にユーザーアカウントシールド値、ベンチマーク商品、アカウント表示名）を更新します。

- **URL**: `openapi/port/v1/accounts/{AccountKey}`
- **メソッド**: PATCH
- **ステータスコード**: 204 No Content

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| AccountKey | string | 必須 | アカウントキー |

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/accounts/account_update_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/account_update_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
AccountKey = "..."
data = {"DisplayName": "MyTestName"}
r = pf.accounts.AccountUpdate(AccountKey=AccountKey, data=data)
client.request(r)
print(r.status_code)
```

### AccountReset

トライアルアカウントをリセットします。ライブ環境では使用できません。

- **URL**: `openapi/port/v1/accounts/{AccountKey}/reset`
- **メソッド**: PUT
- **ステータスコード**: 204 No Content

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| AccountKey | string | 必須 | アカウントキー |

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/accounts/account_reset_body.json)

#### レスポンス

レスポンスデータはありません。

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
AccountKey = "..."
data = {'NewBalance': '1000000'}
r = pf.accounts.AccountReset(AccountKey=AccountKey, data=data)
client.request(r)
print(r.status_code)
```

### SubscriptionCreate

サブスクリプションを設定し、リクエストパラメータで指定されたアカウントのリストを含む初期スナップショットを返します。

- **URL**: `openapi/port/v1/accounts/subscriptions/`
- **メソッド**: POST
- **ステータスコード**: 201 Created

#### リクエスト

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/accounts/subscription_create_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/subscription_create_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
data = {
    "Arguments": {
        "ClientKey": "..."
    },
    "ContextId": "explorer_1551455553043",
    "ReferenceId": "I_213"
}
r = pf.accounts.SubscriptionCreate(data=data)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### SubscriptionRemoveByTag

特定のタグでマークされた現在のセッションのすべてのサブスクリプションを削除し、サーバー上のすべてのリソースを解放します。

- **URL**: `openapi/port/v1/accounts/subscriptions/{ContextId}/`
- **メソッド**: DELETE
- **ステータスコード**: 202 Accepted

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| ContextId | string | 必須 | コンテキストID |
| params | dict | 必須 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accounts/subscription_remove_by_tag_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/subscription_remove_by_tag_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
ContextId = "..."
params = {"ClientKey": "..."}
r = pf.accounts.SubscriptionRemoveByTag(ContextId=ContextId, params=params)
client.request(r)
print(r.status_code)
```

### SubscriptionRemoveById

サブスクリプションIDで識別される現在のセッションのサブスクリプションを削除します。

- **URL**: `openapi/port/v1/accounts/subscriptions/{ContextId}/{ReferenceId}/`
- **メソッド**: DELETE
- **ステータスコード**: 202 Accepted

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| ContextId | string | 必須 | コンテキストID |
| ReferenceId | string | 必須 | リファレンスID |

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accounts/subscription_remove_by_id_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
ContextId = "..."
ReferenceId = "..."
r = pf.accounts.SubscriptionRemoveById(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)
print(r.status_code)
```
