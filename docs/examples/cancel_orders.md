# 注文キャンセルワークフロー

この例では、`endpoints.trading.orders` モジュールを使用して、既存の注文をキャンセルする方法を示します。

## 前提条件

*   有効なアクセストークン
*   キャンセルしたい注文の `OrderId`
*   取引可能な口座の `AccountKey`

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.session import account_info

# 1. クライアントの初期化
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. アカウント情報の取得
ai = account_info(client)
AccountKey = ai.AccountKey

# 3. キャンセル対象の注文ID
# 実際の OrderId に置き換えてください
order_ids = ["76703539", "76703544"]

# 4. リクエストの作成
# DELETE /openapi/trade/v2/orders/{OrderIds}
# 複数の注文を一度にキャンセルできます
r = tr.orders.CancelOrders(
    OrderIds=",".join(order_ids),
    params={'AccountKey': AccountKey}
)

# 5. リクエストの実行
try:
    rv = client.request(r)
    print("キャンセルリクエスト成功:")
    print(json.dumps(rv, indent=2))
except Exception as e:
    print(f"キャンセル失敗: {e}")
```

## 解説

1.  `saxo_openapi.endpoints.trading.orders.CancelOrders` クラスを使用します。
2.  `OrderIds` パラメータには、キャンセルしたい注文IDをカンマ区切りの文字列で指定します。
3.  `params` に `AccountKey` を指定する必要があります。
4.  リクエストが成功すると、キャンセル受付の結果が返されます。
