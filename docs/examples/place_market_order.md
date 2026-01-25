# 成行注文発注ワークフロー

この例では、`contrib.orders` モジュールを使用して FX の成行注文を発注する方法を示します。

## 前提条件

*   有効なアクセストークン
*   取引可能な口座の `AccountKey`

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.orders import (
    MarketOrderFxSpot,
    tie_account_to_order
)
from saxo_openapi.contrib.session import account_info

# 1. クライアントの初期化
# ⚠️ セキュリティ注意: トークンは環境変数から読み込むことを推奨
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. アカウント情報の取得（AccountKeyが必要）
# 自動的に最初のアカウントを取得します
ai = account_info(client)
AccountKey = ai.AccountKey
print(f"Using AccountKey: {AccountKey}")

# 3. 注文スペックの作成
# EURUSD (Uic=21) を 10,000 単位購入
order_spec = MarketOrderFxSpot(
    Uic=21,
    Amount=10000
)

# 4. アカウントの紐付け
# 注文には AccountKey が必須です
order_spec = tie_account_to_order(AccountKey, order_spec)

# 5. リクエストの作成
# POST /openapi/trade/v2/orders
r = tr.orders.Order(data=order_spec)

# 6. リクエストの実行
try:
    rv = client.request(r)
    print("注文成功:")
    print(json.dumps(rv, indent=2))
    print(f"OrderId: {rv['OrderId']}")
except Exception as e:
    print(f"注文失敗: {e}")
```

## 解説

1.  `contrib.session.account_info` を使用して、現在のユーザーの `AccountKey` を取得します。
2.  `contrib.orders.MarketOrderFxSpot` を使用して、FXスポットの成行注文パラメータを作成します。
    *   `Uic=21`: EURUSD の識別子
    *   `Amount=10000`: 取引数量
3.  `tie_account_to_order` ヘルパーを使用して、注文パラメータに `AccountKey` を追加します。
4.  `saxo_openapi.endpoints.trading.orders.Order` エンドポイントを使用して、注文リクエストを作成します。
5.  リクエストを実行し、結果（`OrderId` など）を表示します。
