# 証拠金監視ワークフロー

この例では、`portfolio.balances` モジュールを使用して、口座の証拠金使用状況を監視する方法を示します。

## 前提条件

*   有効なアクセストークン
*   監視したい口座の `AccountKey`（または `ClientKey`）

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.portfolio as pf
from saxo_openapi.contrib.session import account_info

# 1. クライアントの初期化
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. アカウント情報の取得
ai = account_info(client)
AccountKey = ai.AccountKey

# 3. リクエストの作成
# GET /openapi/port/v1/balances
# 特定のアカウントのバランス情報を取得します
r = pf.balances.AccountBalances(
    params={'AccountKey': AccountKey}
)

# 4. リクエストの実行と証拠金情報の抽出
try:
    rv = client.request(r)
    
    # AccountBalances はリストを返します（複数アカウントの可能性があるため）
    # ここでは最初のアカウントを使用します
    balance_data = rv[0]
    
    # 重要な指標の抽出
    total_value = balance_data['TotalValue']           # 口座資産評価額
    cash_available = balance_data['CashAvailableForTrading'] # 取引可能現金
    margin_used = balance_data['MarginUsedByCurrentPositions'] # 使用中証拠金
    margin_utilization = balance_data['MarginUtilizationPct']  # 証拠金使用率 (%)
    
    print(f"=== 口座状況 (Account: {AccountKey}) ===")
    print(f"資産評価額: {total_value:,.2f}")
    print(f"取引可能額: {cash_available:,.2f}")
    print(f"使用証拠金: {margin_used:,.2f}")
    print(f"証拠金使用率: {margin_utilization:.2f}%")
    
    # 警告ロジックの例
    if margin_utilization > 80.0:
        print("⚠️ 警告: 証拠金使用率が80%を超えています！")
        
except Exception as e:
    print(f"取得失敗: {e}")
```

## 解説

1.  `saxo_openapi.endpoints.portfolio.balances.AccountBalances` クラスを使用します。
2.  `params` に `AccountKey` を指定して、特定のアカウントの情報を取得します（指定しない場合はアクセス可能な全アカウントが返されます）。
3.  レスポンスには多くのフィールドが含まれますが、特に重要なのは以下の通りです：
    *   `TotalValue`: 含み益を含めた現在の口座価値
    *   `MarginUsedByCurrentPositions`: 現在のポジション維持に必要な証拠金
    *   `MarginUtilizationPct`: 証拠金使用率。100%に近づくと強制ロスカットの危険があります。
