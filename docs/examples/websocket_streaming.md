# WebSocket ストリーミングワークフロー

この例では、WebSocket を使用してリアルタイムの価格データや通知を受信する方法を示します。

## 前提条件

*   有効なアクセストークン
*   `websocket-client` ライブラリ
    ```bash
    uv pip install websocket-client
    ```
*   `saxo_openapi` ライブラリ

## コード例

```python
import json
import threading
import time
import websocket
from saxo_openapi import API
import saxo_openapi.endpoints.rootservices as rs
import saxo_openapi.endpoints.trading as tr
from saxo_openapi.contrib.ws.stream import decode_ws_msg

# 設定
# ⚠️ セキュリティ注意: トークンは環境変数から読み込むことを推奨
TOKEN = "YOUR_ACCESS_TOKEN"
CONTEXT_ID = "MyApp_Context_001"
REF_ID = "My_Price_Sub_001"

# 1. クライアント初期化
client = API(access_token=TOKEN)

# 2. WebSocket 接続ハンドラ
def on_message(ws, message):
    # バイナリメッセージをデコード
    for msg in decode_ws_msg(message):
        if msg['refid'] == REF_ID:
            # 価格更新データの処理
            payload = msg['msg']
            print(f"Price Update: {json.dumps(payload, indent=2)}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Closed ###")

def on_open(ws):
    print("### Connected ###")
    # 接続確立後にサブスクリプションを作成することも可能ですが、
    # 通常は接続前に REST API で作成するか、接続後に作成します。
    # ここでは別スレッドでサブスクリプションを作成する例を示します。
    threading.Thread(target=create_subscription).start()

# 3. サブスクリプション作成関数（REST API）
def create_subscription():
    # 少し待ってから作成（WS接続確立を確実にするため）
    time.sleep(2)
    
    # EURUSD (Uic=21) の価格を購読
    data = {
        "ContextId": CONTEXT_ID,
        "ReferenceId": REF_ID,
        "Arguments": {
            "Uic": 21,
            "AssetType": "FxSpot"
        }
    }
    
    # InfoPrices サブスクリプションエンドポイント
    # 注意: 以下は概念的な例です。実際のエンドポイントクラスを使用してください。
    # 例: saxo_openapi.endpoints.trading.infoprices.InfoPriceSubscription
    
    # r = tr.infoprices.InfoPriceSubscription(data=data)
    # 実際のエンドポイントが存在しない場合は、適切なエンドポイントを確認してください。
    # ここでは例として汎用的なリクエスト構造を示しています。
    pass
    
    # try:
    #     client.request(r)
    #     print(f"Subscription created for {REF_ID}")
    # except Exception as e:
    #     print(f"Subscription failed: {e}")

# 4. WebSocket 接続開始
url = f"wss://sim-streaming.saxobank.com/sim/openapi/streamingws/connect?contextId={CONTEXT_ID}&authorization={TOKEN}"

ws = websocket.WebSocketApp(
    url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# ブロッキング実行
ws.run_forever()
```

## 解説

1.  **ContextId と ReferenceId**: ストリーミングセッションを識別するための `ContextId` と、個々のデータストリーム（サブスクリプション）を識別するための `ReferenceId` を定義します。
2.  **WebSocket 接続**: `websocket-client` を使用して Saxo Bank のストリーミングサーバーに接続します。URL には `ContextId` と認証トークンを含めます。
3.  **メッセージデコード**: `on_message` コールバック内で、`saxo_openapi.contrib.ws.stream.decode_ws_msg` を使用してバイナリメッセージをデコードします。
4.  **サブスクリプション作成**: WebSocket 接続とは別に、REST API を使用してデータの購読（サブスクリプション）を開始します。このリクエストボディには、WebSocket 接続と同じ `ContextId` と、このデータストリーム用の `ReferenceId` を指定します。
5.  **データ受信**: サブスクリプションが成功すると、サーバーは WebSocket 経由で指定された `ReferenceId` タグ付きのデータを送信し始めます。

## 注意点

*   Saxo Bank の WebSocket プロトコルはバイナリ形式を使用するため、デコードが必要です。
*   サブスクリプションは REST API 経由で管理（作成、削除）されます。
*   接続が切断された場合、再接続後にサブスクリプションを再作成する必要がある場合があります（サーバー側の状態によります）。
