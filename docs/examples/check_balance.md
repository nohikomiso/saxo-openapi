# 残高確認ワークフロー

この例では、ログイン中のユーザーの口座残高を確認する方法を示します。

## 前提条件

*   有効なアクセストークン
*   `saxo_openapi` ライブラリがインストールされていること

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.portfolio as pf

# 1. クライアントの初期化
# ⚠️ セキュリティ注意: トークンは環境変数から読み込むことを推奨
# import os
# token = os.getenv("SAXO_ACCESS_TOKEN")
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. リクエストの作成
# AccountBalancesMe: ログインユーザーの全口座の残高を取得
r = pf.balances.AccountBalancesMe()

# 3. リクエストの実行
try:
    rv = client.request(r)
    
    # 4. 結果の表示
    print(json.dumps(rv, indent=2))

    # 特定の口座の現金残高を表示する例
    for account_data in rv.get('Data', []):
        account_id = account_data.get('AccountId')
        cash_available = account_data.get('CashAvailableForTrading')
        currency = account_data.get('Currency')
        
        print(f"Account: {account_id}")
        print(f"  Cash Available: {cash_available} {currency}")
        
except Exception as e:
    print(f"Error checking balance: {e}")
```

## 解説

1.  `API` クラスをアクセストークンで初期化します。
2.  `saxo_openapi.endpoints.portfolio.balances.AccountBalancesMe` エンドポイントクラスをインスタンス化します。これは `/openapi/port/v1/balances/me` への GET リクエストを表します。
3.  `client.request(r)` で API リクエストを送信し、レスポンス（JSON）を取得します。
4.  レスポンスデータから必要な情報（口座ID、取引可能現金残高、通貨など）を抽出して表示します。
