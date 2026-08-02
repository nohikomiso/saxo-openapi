# クイックスタートガイド

5分で `saxo_api_client` ライブラリの基本的な使い方を習得できます。

## 前提条件

- Python 3.13 以上
- Saxo Bank アカウント
- アクセストークン ([認証ガイド](authentication.md) を参照)

## ステップ 1: インストール

**pip を使用する場合**
```bash
pip install git+https://github.com/nohikomiso/saxo-api-client.git
```

**uv を使用する場合**
```bash
uv add git+https://github.com/nohikomiso/saxo-api-client.git
```

## ステップ 2: アクセストークンの準備

Saxo Developer Portal からアクセストークンを取得します。詳細な手順は [認証ガイド](authentication.md) をご覧ください。

セキュリティのため、トークンは環境変数から読み込むことを推奨します:

```bash
export SAXO_ACCESS_TOKEN="your_access_token_here"
```

## ステップ 3: 最初のリクエスト (残高確認)

以下のコードで、ログイン中のユーザーの口座残高を取得できます:

```python
import json
import os
from saxo_api_client import API
import saxo_api_client.endpoints.portfolio as pf

# 1. クライアントの初期化
token = os.getenv("SAXO_ACCESS_TOKEN")

# Simulation（Developer 24h トークン等）— 既定
client = API(access_token=token)

# Live 口座トークンの場合は environment を明示
# client = API(access_token=token, environment="live")

# OAuth 保存 JSON から（ファイル名または base_uri から推論）
# from saxo_api_client.contrib.client import SaxoClient
# client = SaxoClient.from_token_file("saxo_token_live_live.json")._api

# 2. リクエストの作成
r = pf.balances.AccountBalancesMe()

# 3. リクエストの実行
rv = client.request(r)

# 4. 結果の表示
print(json.dumps(rv, indent=2))
```

## ステップ 4: レスポンスの処理

レスポンスは JSON 形式で返されます。特定のフィールドにアクセスする例:

```python
# 各口座の残高を表示
for account_data in rv.get('Data', []):
    account_id = account_data.get('AccountId')
    cash_available = account_data.get('CashAvailableForTrading')
    currency = account_data.get('Currency')
    
    print(f"Account: {account_id}")
    print(f"  Cash Available: {cash_available} {currency}")
```

レスポンスの詳細な構造は [JSON Schema](schemas/portfolio/balances/account_balances_me_response.json) で確認できます。

## ステップ 5: 次のステップ

### ワークフロー例を試す

実際のユースケースに基づいた例:

- [成行注文の発注](examples/place_market_order.md)
- [ポジション決済](examples/close_position.md)
- [ポジション監視](examples/monitor_positions.md)
- [WebSocket ストリーミング](examples/websocket_streaming.md)

### API リファレンスを参照

カテゴリ別の全エンドポイント:

- [Portfolio](api/portfolio/README.md) - 残高、ポジション、口座情報
- [Trading](api/trading/README.md) - 注文発注、価格情報
- [ReferenceData](api/referencedata/README.md) - 銘柄検索、通貨情報

### Contrib モジュールを活用

新規建ては `PositionOpen`、決済は `PositionClose`（または `SaxoClient.open_*` / `close_*`）を使います。

```python
from saxo_api_client.contrib.orders import PositionOpen, TakeProfitDetails, StopLossDetails

# EURUSD 新規買い (TP/SL 付き) — is_force_open は必須
order = PositionOpen.market(
    uic=21,
    amount=10000,
    asset_type="FxSpot",
    buy_sell="Buy",
    is_force_open=False,
    take_profit_on_fill=TakeProfitDetails(price=1.14),
    stop_loss_on_fill=StopLossDetails(price=1.12),
)
```

ForceOpen 決済や FIFO 相殺の選び方は [Contrib Orders](contrib/orders.md) と [ポジション決済例](examples/close_position.md) を参照してください。

## トラブルシューティング

### 認証エラー

```
HTTP 401 Unauthorized
```

- アクセストークンが有効か確認
- トークンの有効期限を確認 (通常 20 分)
- 必要に応じてトークンを再取得

詳細は [認証ガイド](authentication.md#トラブルシューティング) を参照。

### インポートエラー

```
ModuleNotFoundError: No module named 'saxo_api_client'
```

- ライブラリがインストールされているか確認:
  ```bash
  pip list | grep saxo
  ```
- 正しい Python 環境を使用しているか確認

## さらに学ぶ

- **[API リファレンス](api/README.md)**: 全エンドポイントの詳細
- **[Contrib モジュール](contrib/orders.md)**: 便利なヘルパークラス
- **[ワークフロー例](examples/)**: 実践的な使用例
- **[Saxo OpenAPI 公式ドキュメント](https://www.developer.saxo/openapi/learn)**: API 仕様
