# Root Services - Subscriptions

このセクションでは、ストリーミングデータの購読（Subscription）を管理するためのエンドポイントを扱います。

- **購読の削除**: 特定のコンテキストIDに関連する複数のアクティブな購読を削除します。

---

## `RemoveMultipleActiveSubscriptions`

現在のセッションの複数の購読を削除し、サーバー上のすべてのリソースを解放します。

### エンドポイント

```
DELETE openapi/root/subscriptions/{ContextId}
```

### パラメータ

| 名前 | 位置 | 説明 |
|------|------|------|
| ContextId | path | 購読を削除する対象のコンテキストID。 |
| params | query | 削除する購読の参照ID（`ReferenceIds`）を指定します。 |

### コード例

```python
import saxo_openapi
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# ContextIdと削除したいReferenceIdsを指定
ContextId = "my_streaming_context"
params = {
    "ReferenceIds": [
        "position_subscription_1",
        "order_subscription_2"
    ]
}

# リクエストの作成と実行
r = saxo_openapi.endpoints.rootservices.subscriptions.RemoveMultipleActiveSubscriptions(
    ContextId=ContextId,
    params=params
)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `202Accepted` を返しますが、レスポンスボディにデータは含まれません。
