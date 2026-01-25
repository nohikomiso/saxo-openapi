# RootServices - Features

## 概要

Featuresエンドポイントは、Saxo Bank OpenAPIで利用可能な機能の可用性を確認・監視するためのエンドポイント群です。リアルタイムでの機能可用性の変更を監視するためのサブスクリプション機能も提供されています。

## エンドポイント一覧

| エンドポイント | HTTPメソッド | 説明 |
|--------------|------------|------|
| Availability | GET | すべての機能の可用性を取得 |
| CreateAvailabilitySubscription | POST | 機能可用性のサブスクリプションを作成 |
| RemoveAvailabilitySubscription | DELETE | 機能可用性のサブスクリプションを削除 |

## クイック例

### 機能の可用性を確認

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices.features as rsft

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 利用可能な機能を取得
request = rsft.Availability()
response = client.request(request)
print(response)
```

## 詳細仕様

### Availability

**説明**: すべての機能の可用性を取得します。

**HTTPメソッド**: GET  
**エンドポイント**: `/openapi/root/v1/features/availability/`

**パラメータ**: なし

**レスポンス**: 機能の可用性リスト

**レスポンススキーマ**: [availability_response.json](../../schemas/rootservices/features/availability_response.json)

**レスポンス例**:

```json
[
  {
    "Available": true,
    "Feature": "News"
  },
  {
    "Available": true,
    "Feature": "GainersLosers"
  },
  {
    "Available": true,
    "Feature": "Calendar"
  },
  {
    "Available": true,
    "Feature": "Chart"
  }
]
```

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices.features as rsft

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rsft.Availability()
rv = client.request(r)
print(rv)
```

---

### CreateAvailabilitySubscription

**説明**: 機能可用性のサブスクリプションを作成します。機能の可用性が変更されたときにストリーミング更新を受け取ることができます。

**HTTPメソッド**: POST  
**エンドポイント**: `/openapi/root/v1/features/availability/subscriptions`  
**期待されるステータスコード**: 201

**パラメータ**:
- `data` (JSON, 必須): サブスクリプション設定

**リクエストボディスキーマ**: [create_availability_subscription_body.json](../../schemas/rootservices/features/create_availability_subscription_body.json)

**リクエストボディ例**:

```json
{
  "Arguments": {},
  "ContextId": "your_context_id",
  "ReferenceId": "your_reference_id"
}
```

**レスポンススキーマ**: [create_availability_subscription_response.json](../../schemas/rootservices/features/create_availability_subscription_response.json)

**レスポンス例**:

```json
{
  "ContextId": "20190305131009595",
  "Format": "application/json",
  "InactivityTimeout": 30,
  "ReferenceId": "features_reference",
  "RefreshRate": 1000,
  "Snapshot": {
    "Data": [
      {
        "Available": true,
        "Feature": "News"
      },
      {
        "Available": true,
        "Feature": "Calendar"
      }
    ]
  },
  "State": "Active"
}
```

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices.features as rsft

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "Arguments": {},
    "ContextId": "your_context_id",
    "ReferenceId": "features_ref"
}

r = rsft.CreateAvailabilitySubscription(data=data)
rv = client.request(r)
print(rv)
```

---

### RemoveAvailabilitySubscription

**説明**: 指定されたリファレンスIDとストリーミングコンテキストIDで識別されるサブスクリプションを削除します。

**HTTPメソッド**: DELETE  
**エンドポイント**: `/openapi/root/v1/features/availability/subscriptions/{ContextId}/{ReferenceId}`  
**期待されるステータスコード**: 202

**パラメータ**:
- `ContextId` (string, 必須): コンテキストID
- `ReferenceId` (string, 必須): リファレンスID

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices.features as rsft

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

context_id = "your_context_id"
reference_id = "features_ref"

r = rsft.RemoveAvailabilitySubscription(
    ContextId=context_id,
    ReferenceId=reference_id
)
rv = client.request(r)
assert r.status_code == r.expected_status
```

## ユースケース

- **機能確認**: アカウントで利用可能な機能をチェック
- **リアルタイム監視**: サブスクリプションを使って機能可用性の変更をリアルタイムで監視
- **機能制限の確認**: 特定の機能（ニュース、チャート、カレンダーなど）が利用可能か判定

## 関連ドキュメント

- [RootServices概要](./README.md)
- [Diagnostics](./diagnostics.md)
- [Sessions](./sessions.md)
