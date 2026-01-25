# AccountGroups

ポートフォリオのアカウントグループを管理するエンドポイント。

## エンドポイント

### AccountGroupDetails

単一のアカウントグループの詳細を取得します。

- **URL**: `openapi/port/v1/accountgroups/{AccountGroupKey}`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| AccountGroupKey | string | 必須 | アカウントグループキー |
| params | dict | 必須 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accountgroups/account_group_details_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accountgroups/account_group_details_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {}  # 必要なパラメータを設定
AccountGroupKey = "..."
r = pf.accountgroups.AccountGroupDetails(AccountGroupKey=AccountGroupKey, params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountGroupsMe

ログインユーザーが所属する特定のクライアント配下のすべてのアカウントグループを取得します。

- **URL**: `openapi/port/v1/accountgroups/me`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 任意 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accountgroups/account_groups_me_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accountgroups/account_groups_me_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {}
r = pf.accountgroups.AccountGroupsMe(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountGroupsList

指定されたクライアントが使用するすべてのアカウントグループのリストを取得します。

- **URL**: `openapi/port/v1/accountgroups/`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 必須 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accountgroups/account_groups_list_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accountgroups/account_groups_list_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {"ClientKey": "..."}
r = pf.accountgroups.AccountGroupsList(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### AccountGroupUpdate

アカウントグループの設定（特にAccountValueProtectionLimit）を更新します。

- **URL**: `openapi/port/v1/accountgroups/{AccountGroupKey}`
- **メソッド**: PATCH
- **ステータスコード**: 204 No Content

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| AccountGroupKey | string | 必須 | アカウントグループキー |
| params | dict | 必須 | クエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/accountgroups/account_group_update_params.json)

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/accountgroups/account_group_update_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/accountgroups/account_group_update_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
AccountGroupKey = "..."
params = {}
data = {}
r = pf.accountgroups.AccountGroupUpdate(
    AccountGroupKey=AccountGroupKey,
    params=params,
    data=data
)
client.request(r)
print(r.status_code)
```
