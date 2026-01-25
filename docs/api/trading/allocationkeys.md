# Allocation Keys

## 概要

Allocation Keys（配分キー）は、注文を複数のアカウント間で配分するための仕組みです。このモジュールでは、配分キーの作成、取得、削除を行うエンドポイントを提供します。

## エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| GetAllocationKeys | GET | 配分キー一覧を取得 |
| GetAllocationKeyDetails | GET | 配分キーの詳細情報を取得 |
| CreateAllocationKey | POST | 配分キーを作成 |
| DeleteAllocationKey | DELETE | 配分キーを削除 |

## GetAllocationKeys

既存の配分キー一覧を取得します。デフォルトでは、現在のクライアントのアクティブな配分キーのみが返されます。

### パラメータ

- **params** (dict, required): クエリパラメータ
  - Status: 配分キーのステータスでフィルタリング

### JSON Schema

- **Params**: [get_allocation_keys_params.json](../../schemas/trading/allocationkeys/get_allocation_keys_params.json)
- **Response**: [get_allocation_keys_response.json](../../schemas/trading/allocationkeys/get_allocation_keys_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 配分キー一覧を取得
params = {
    "Status": "Active"
}
r = tr.allocationkeys.GetAllocationKeys(params=params)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## GetAllocationKeyDetails

特定の配分キーの詳細情報を取得します。

### パラメータ

- **AllocationKeyId** (string, required): 配分キーID

### JSON Schema

- **Response**: [get_allocation_key_details_response.json](../../schemas/trading/allocationkeys/get_allocation_key_details_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 配分キーの詳細を取得
AllocationKeyId = "227"
r = tr.allocationkeys.GetAllocationKeyDetails(
    AllocationKeyId=AllocationKeyId)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## CreateAllocationKey

新しい配分キーを作成します。

### パラメータ

- **data** (dict, required): リクエストボディのパラメータ
  - AllocationKeyName: 配分キー名
  - AllocationUnitType: 配分単位タイプ（Percentage, Amount等）
  - MarginHandling: マージン処理方法
  - OneTime: 一回限りの使用かどうか
  - OwnerAccountKey: 所有者アカウントキー
  - ParticipatingAccountsInfo: 参加アカウント情報のリスト

### JSON Schema

- **Body**: [create_allocation_key_body.json](../../schemas/trading/allocationkeys/create_allocation_key_body.json)
- **Response**: [create_allocation_key_response.json](../../schemas/trading/allocationkeys/create_allocation_key_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 配分キーを作成
data = {
    "AllocationKeyName": "MyAllocation_Key",
    "AllocationUnitType": "Percentage",
    "MarginHandling": "Reduce",
    "OneTime": True,
    "OwnerAccountKey": "YOUR_ACCOUNT_KEY",
    "ParticipatingAccountsInfo": [
        {
            "AcceptRemainderAmount": True,
            "AccountKey": "ACCOUNT_KEY_1",
            "Priority": 1,
            "UnitValue": 10.0
        },
        {
            "AcceptRemainderAmount": False,
            "AccountKey": "ACCOUNT_KEY_2",
            "Priority": 1,
            "UnitValue": 90.0
        }
    ]
}
r = tr.allocationkeys.CreateAllocationKey(data=data)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## DeleteAllocationKey

配分キーを削除します。

### パラメータ

- **AllocationKeyId** (string, required): 配分キーID

### JSON Schema

- **Response**: [delete_allocation_key_response.json](../../schemas/trading/allocationkeys/delete_allocation_key_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 配分キーを削除
AllocationKeyId = "227"
r = tr.allocationkeys.DeleteAllocationKey(
    AllocationKeyId=AllocationKeyId)
client.request(r)
assert r.status_code == r.expected_status
```

## 関連エンドポイント

- [Trading Orders](../trading/orders.md) - 配分キーを使用した注文
