# デルタヘッジワークフロー例

この例では、オプションポジションのデルタを計算し、原資産（FXスポット）でヘッジ注文を出すという、より高度なワークフローを示します。
※ デルタ計算ロジックは簡略化されたダミーです。

## 前提条件

*   有効なアクセストークン
*   オプションポジションを保有していること

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.portfolio as pf
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.orders import MarketOrderFxSpot, tie_account_to_order
from saxo_openapi.contrib.session import account_info

# 1. クライアント初期化
# ⚠️ セキュリティ注意: トークンは環境変数から読み込むことを推奨
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)
ai = account_info(client)
AccountKey = ai.AccountKey

# 2. デルタ計算関数（ダミー）
def calculate_portfolio_delta(positions):
    total_delta = 0
    for pos in positions:
        # 実際にはここで Black-Scholes モデルなどを使用してデルタを計算します。
        # 実用的な実装には scipy.stats.norm や mibian ライブラリなどが推奨されます。
        # 例:
        # import mibian
        # c = mibian.BS([CurrentPrice, StrikePrice, InterestRate, DaysToExpiration], volatility=Vol)
        # delta = c.callDelta if is_call else c.putDelta
        
        # ここではポジションの Greeks データが API から返されていると仮定
        # または簡易的に計算
        
        # 例: オプションポジションの場合
        if pos['NetPositionBase']['AssetType'] == 'FxVanillaOption':
            # APIからGreeksが取得できる場合の例（架空のフィールド）
            # delta = pos['Greeks']['Delta'] 
            delta = 0.5 # ダミー値
            amount = pos['NetPositionBase']['Amount']
            total_delta += delta * amount
            
    return total_delta

# 3. ポジション取得
r = pf.netpositions.NetPositionsMe()
rv = client.request(r)
positions = rv.get('Data', [])

# 4. 現在のデルタ算出
current_delta = calculate_portfolio_delta(positions)
print(f"Current Portfolio Delta: {current_delta}")

# 5. ヘッジ判断
# 目標デルタを 0 とする（デルタニュートラル）
target_delta = 0
hedge_needed = target_delta - current_delta

print(f"Hedge Needed: {hedge_needed}")

# 閾値を設けて、小さな変動ではヘッジしない
THRESHOLD = 1000

if abs(hedge_needed) > THRESHOLD:
    print("Executing hedge order...")
    
    # ヘッジ注文の作成（FXスポットでヘッジ）
    # Uic=21 (EURUSD) と仮定
    
    # hedge_needed > 0 なら買い（Buy）、< 0 なら売り（Sell）
    # MarketOrderFxSpot は Amount の符号で売買を判定
    
    order_spec = MarketOrderFxSpot(
        Uic=21,
        Amount=hedge_needed
    )
    
    order_spec = tie_account_to_order(AccountKey, order_spec)
    
    # 注文発注
    r_order = tr.orders.Order(data=order_spec)
    
    try:
        rv_order = client.request(r_order)
        print(f"Hedge order placed: {rv_order['OrderId']}")
    except Exception as e:
        print(f"Hedge order failed: {e}")
        
else:
    print("No hedge needed (within threshold).")
```

## 解説

このワークフローは以下のステップを実行します：

1.  **情報収集**: 現在のポートフォリオ（ポジション）情報を取得します。
2.  **分析・計算**: 取得したポジション情報に基づいて、ポートフォリオ全体のリスク指標（ここではデルタ）を計算します。
3.  **意思決定**: 現在のリスク指標と目標値（デルタニュートラル＝0）を比較し、ヘッジが必要な数量を算出します。
4.  **アクション**: ヘッジが必要な場合、`contrib.orders` を使用して適切なヘッジ注文（原資産の売買）を自動的に生成し、発注します。

これはアルゴリズム取引の基本的なループ（Observe -> Orient -> Decide -> Act）の一例です。
