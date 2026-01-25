# RootServices - Sessions

## 概要

Sessionsエンドポイントは、Saxo Bank OpenAPIのセッション機能を管理するためのエンドポイント群です。セッション能力（capabilities）の取得、変更、およびリアルタイム監視のためのサブスクリプション機能を提供しています。

## エンドポイント一覧

| エンドポイント | HTTPメソッド | 説明 |
|--------------|------------|------|
| GetSessionCapabilities | GET | セッション能力を取得 |
| ChangeSessionCapabilities | PUT | セッション能力を変更 |
| CreateSessionCapabilitiesSubscription | POST | セッション能力変更のサブスクリプションを作成 |
| RemoveSessionCapabilitiesSubscription | DELETE | セッション能力変更のサブスクリプションを削除 |

## クイック例

### セッション能力を取得

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# セッション能力を取得
request = rs.sessions.GetSessionCapabilities()
response = client.request(request)
print(response)
```

## 詳細仕様

### GetSessionCapabilities

**説明**: 現在のセッションの能力を取得します。

**HTTPメソッド**: GET  
**エンドポイント**: `/openapi/root/v1/sessions/capabilities/`

**パラメータ**: なし

**レスポンススキーマ**: [get_session_capabilities_response.json](../../schemas/rootservices/sessions/get_session_capabilities_response.json)

**レスポンス例**:

```json
{
  "DataLevel": "Standard",
  "TradeLevel": "OrdersOnly"
}
```

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.sessions.GetSessionCapabilities()
rv = client.request(r)
print(rv)
```

---

### ChangeSessionCapabilities

**説明**: セッション能力を変更します。

**HTTPメソッド**: PUT  
**エンドポイント**: `/openapi/root/v1/sessions/capabilities/`  
**期待されるステータスコード**: 202

**パラメータ**:
- `data` (JSON, 必須): 新しいセッション能力の設定

**リクエストボディスキーマ**: [change_session_capabilities_body.json](../../schemas/rootservices/sessions/change_session_capabilities_body.json)

**リクエストボディ例**:

```json
{
  "TradeLevel": "FullTradingAndChat"
}
```

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "TradeLevel": "FullTradingAndChat"
}

r = rs.sessions.ChangeSessionCapabilities(data=data)
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### CreateSessionCapabilitiesSubscription

**説明**: セッション能力の変更を監視するための新しいサブスクリプションを作成します。データストリームは、この時点から更新を配信します。

**HTTPメソッド**: POST  
**エンドポイント**: `/openapi/root/v1/sessions/events/subscriptions/`  
**期待されるステータスコード**: 201

**パラメータ**:
- `data` (JSON, 必須): サブスクリプション設定

**リクエストボディスキーマ**: [create_session_capabilities_subscription_body.json](../../schemas/rootservices/sessions/create_session_capabilities_subscription_body.json)

**リクエストボディ例**:

```json
{
  "Arguments": {
    "ClientKey": "your_client_key"
  },
  "ContextId": "your_context_id",
  "ReferenceId": "session_caps_ref"
}
```

**レスポンススキーマ**: [create_session_capabilities_subscription_response.json](../../schemas/rootservices/sessions/create_session_capabilities_subscription_response.json)

**レスポンス例**:

```json
{
  "ContextId": "20190305131009595",
  "Format": "application/json",
  "InactivityTimeout": 30,
  "ReferenceId": "session_caps_ref",
  "RefreshRate": 1000,
  "Snapshot": {
    "DataLevel": "Standard",
    "TradeLevel": "OrdersOnly"
  },
  "State": "Active"
}
```

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "Arguments": {"ClientKey": "your_client_key"},
    "ContextId": "your_context_id",
    "ReferenceId": "session_caps_ref"
}

r = rs.sessions.CreateSessionCapabilitiesSubscription(data=data)
rv = client.request(r)
print(rv)
```

---

### RemoveSessionCapabilitiesSubscription

**説明**: 指定されたリファレンスIDとストリーミングコンテキストIDで識別されるサブスクリプションを削除します。

**HTTPメソッド**: DELETE  
**エンドポイント**: `/openapi/root/v1/sessions/events/subscriptions/{ContextId}/{ReferenceId}`  
**期待されるステータスコード**: 202

**パラメータ**:
- `ContextId` (string, 必須): コンテキストID
- `ReferenceId` (string, 必須): リファレンスID

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

context_id = "your_context_id"
reference_id = "session_caps_ref"

r = rs.sessions.RemoveSessionCapabilitiesSubscription(
    ContextId=context_id,
    ReferenceId=reference_id
)
rv = client.request(r)
assert r.status_code == r.expected_status
```

## ユースケース

- **セッション情報の確認**: 現在のセッションのデータレベルやトレードレベルを確認
- **権限の変更**: セッション中にトレード権限レベルを動的に変更
- **リアルタイム監視**: サブスクリプションを使ってセッション能力の変更をリアルタイムで監視
- **セキュリティ管理**: セッションの能力を適切に管理し、必要最小限の権限で動作

## セッション能力の値

### DataLevel
- `Standard`: 標準データレベル

### TradeLevel
- `OrdersOnly`: 注文のみ可能
- `FullTradingAndChat`: 完全な取引とチャット機能

## 関連ドキュメント

- [RootServices概要](./README.md)
- [Diagnostics](./diagnostics.md)
- [Features](./features.md)
