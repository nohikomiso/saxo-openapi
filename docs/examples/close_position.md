# ポジション決済ワークフロー

この例では、保有しているポジションを決済（クローズ）する方法を示します。
Saxo API では、ポジションの決済は「反対売買の注文」として扱われます。

## 前提条件

*   有効なアクセストークン
*   決済したいポジションの `PositionId`
*   ポジションの数量とUic

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.orders import (
    MarketOrderFxSpot,
    tie_account_to_order,
    direction_invert
)
from saxo_openapi.contrib.session import account_info

# 1. クライアントの初期化
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. アカウント情報の取得
ai = account_info(client)
AccountKey = ai.AccountKey

# 3. 決済対象のポジション情報
# 実際にはポートフォリオエンドポイントから取得した値を使用します
position_id = "12345678"
uic = 21           # EURUSD
amount = 10000     # 保有数量
current_direction = "Buy" # 現在のポジション方向

# 4. 反対売買の注文スペック作成
# 決済のために、現在のポジションと逆方向の注文を作成します
# direction_invert ヘルパーを使うと便利ですが、
# MarketOrderFxSpot は Amount の符号で売買を判断するため、
# 単に Amount の符号を反転させるだけで十分です。

close_amount = -amount if current_direction == "Buy" else abs(amount)

# 成行注文で決済する場合
order_spec = MarketOrderFxSpot(
    Uic=uic,
    Amount=close_amount
)

# 5. アカウントとポジションIDの紐付け
# PositionId を指定することで、特定のポジションに対する決済注文であることを明示します
# これにより、Netting モードでも意図したポジションを決済できます
order_spec = tie_account_to_order(AccountKey, order_spec)
order_spec['PositionId'] = position_id

# 6. リクエストの作成
r = tr.orders.Order(data=order_spec)

# 7. リクエストの実行
try:
    rv = client.request(r)
    print("決済注文成功:")
    print(json.dumps(rv, indent=2))
except Exception as e:
    print(f"決済失敗: {e}")
```

## 解説

1.  ポジションを決済するには、そのポジションと「逆方向」かつ「同数量」の注文を出します。
2.  `MarketOrderFxSpot` などの注文ヘルパーを使用し、数量（Amount）の符号を反転させて指定します。
3.  **重要**: `PositionId` を注文パラメータに含めることで、システムに「この注文は特定のポジションを決済するためのもの」と伝えます。これにより、意図しない新規ポジションの構築を防ぎます。
4.  `tie_account_to_order` を使用した後、手動で `PositionId` を追加します。
