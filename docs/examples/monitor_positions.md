# ポジション監視ワークフロー

この例では、現在の保有ポジションを取得し、その損益状況を監視する方法を示します。

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
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. ポジション取得リクエストの作成
# NetPositionsMe: ログインユーザーのネットポジションを取得
r = pf.netpositions.NetPositionsMe()

# 3. リクエストの実行
try:
    rv = client.request(r)

    # 4. ポジション情報の表示
    print(f"Total Positions: {rv.get('__count', 0)}")

    for pos in rv.get('Data', []):
        net_pos_id = pos['NetPositionId']
        instrument = pos['DisplayAndFormat']['Description']
        amount = pos['NetPositionBase']['Amount']
        open_price = pos['NetPositionBase']['OpenPrice']
        current_price = pos['NetPositionView']['CurrentPrice']
        pl = pos['NetPositionView']['ProfitLossOnTrade']
        
        print("-" * 40)
        print(f"ID: {net_pos_id}")
        print(f"Instrument: {instrument}")
        print(f"Amount: {amount}")
        print(f"Open Price: {open_price}")
        print(f"Current Price: {current_price}")
        print(f"P/L: {pl}")

    # 5. 特定の銘柄（例: EURUSD）のポジションのみフィルタリングする場合
    # クライアント側でフィルタリングするか、APIパラメータを使用可能な場合は使用します
    # NetPositionsMe はパラメータでのフィルタリングをサポートしていない場合が多いですが、
    # リスト内包表記で簡単にフィルタリングできます。

    eurusd_positions = [
        p for p in rv.get('Data', []) 
        if "EURUSD" in p['DisplayAndFormat']['Symbol']
    ]

    print(f"\nEURUSD Positions: {len(eurusd_positions)}")

except Exception as e:
    print(f"Error monitoring positions: {e}")
```

## 解説

1.  `saxo_openapi.endpoints.portfolio.netpositions.NetPositionsMe` を使用して、現在のネットポジション一覧を取得します。
2.  レスポンスの `Data` リストをループし、各ポジションの詳細情報（銘柄名、数量、建玉価格、現在価格、損益など）を表示します。
3.  必要に応じて、取得したデータから特定の銘柄のポジションをフィルタリングします。

## 補足

リアルタイムでポジションの変動を監視したい場合は、ポーリング（定期的なリクエスト）を行うか、WebSocket ストリーミング（`docs/examples/websocket_streaming.md` 参照）を使用することをお勧めします。
