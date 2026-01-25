# Clients

クライアント情報を管理するエンドポイント。

## エンドポイント

### ClientDetailsMe

ログインユーザーのクライアント詳細を取得します。

- **URL**: `openapi/port/v1/clients/me`
- **メソッド**: GET

#### リクエスト

パラメータはありません。

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/clients/client_details_me_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
r = pf.clients.ClientDetailsMe()
client.request(r)
print(json.dumps(r.response, indent=2))
```

### ClientDetails

指定されたクライアントの詳細を取得します。

- **URL**: `openapi/port/v1/clients/{ClientKey}`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| ClientKey | string | 必須 | クライアントキー |

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/clients/client_details_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
ClientKey = "..."
r = pf.clients.ClientDetails(ClientKey=ClientKey)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### ClientDetailsUpdate

クライアント自身のポジションネッティングモードなどを更新します。

- **URL**: `openapi/port/v1/clients/me`
- **メソッド**: PATCH
- **ステータスコード**: 204 No Content

#### リクエスト

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/clients/client_details_update_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/clients/client_details_update_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
data = {
    "AccountValueProtectionLimit": 10000.0,
    "PositionNettingMode": "Netting"
}
r = pf.clients.ClientDetailsUpdate(data=data)
client.request(r)
print(r.status_code)
```

### ClientDetailsByOwner

特定のオーナー配下のクライアント詳細を取得します。

- **URL**: `openapi/port/v1/clients/`
- **メソッド**: GET

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 必須 | OwnerKeyを含むクエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/clients/client_details_by_owner_params.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/clients/client_details_by_owner_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {"OwnerKey": "..."}
r = pf.clients.ClientDetailsByOwner(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### ClientSwitchPosNettingMode

IBがクライアントに代わってポジションネッティングモードやアカウント保護制限を変更します。

- **URL**: `openapi/port/v1/clients/`
- **メソッド**: PATCH
- **ステータスコード**: 204 No Content

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| params | dict | 必須 | ClientKeyを含むクエリパラメータ |

[クエリパラメータスキーマ](../../schemas/portfolio/clients/client_switch_pos_netting_mode_params.json)

**ボディ**

[リクエストボディスキーマ](../../schemas/portfolio/clients/client_switch_pos_netting_mode_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/portfolio/clients/client_switch_pos_netting_mode_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.portfolio as pf
import json

client = saxo_openapi.API(access_token=...)
params = {"ClientKey": "..."}
data = {
    "NewPositionNettingMode": "Netting"
}
r = pf.clients.ClientSwitchPosNettingMode(params=params, data=data)
client.request(r)
print(r.status_code)
```
