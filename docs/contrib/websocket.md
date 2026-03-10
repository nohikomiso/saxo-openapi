# Contrib WebSocket

`saxo_openapi.contrib.ws` モジュールは、Saxo Bank OpenAPI の WebSocket ストリーミングデータを処理するためのヘルパー関数を提供します。

## 概要

Saxo Bank の WebSocket ストリーミングは、バイナリ形式でメッセージを送信します。このモジュールは、そのバイナリデータを解析し、Python で扱いやすい辞書形式に変換する機能を提供します。

## インポート

```python
from saxo_openapi.contrib.ws.stream import decode_ws_msg
```

## 関数

### decode_ws_msg

WebSocket から受信した生のバイナリデータをデコードします。
ストリームには異なるソース（ReferenceId で識別）からのメッセージが含まれる場合があるため、ジェネレータとして実装されており、メッセージごとに辞書を返します。

```python
def decode_ws_msg(raw: bytes) -> Generator[dict, None, None]:
    ...
```

**引数:**
*   `raw` (bytes): WebSocket から受信した生のバイナリデータ。

**戻り値:**
*   `Generator[dict]`: デコードされたメッセージのジェネレータ。各メッセージは以下の構造を持ちます：

```python
{
    'refid': str,       # サブスクリプション作成時に指定した ReferenceId
    'msgId': int,       # メッセージ識別子
    'msg': dict | Any   # 解析された JSON ペイロード、または生のペイロード
}
```

## 使用例

一般的な WebSocket クライアント（例: `websocket-client` ライブラリ）と組み合わせて使用する例です。

```python
import websocket
from saxo_openapi.contrib.ws.stream import decode_ws_msg

def on_message(ws, message):
    # 受信したバイナリメッセージをデコード
    for msg in decode_ws_msg(message):
        print(f"Reference ID: {msg['refid']}")
        print(f"Payload: {msg['msg']}")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

# WebSocket 接続（認証トークンが必要）
token = "YOUR_ACCESS_TOKEN"
context_id = "YOUR_CONTEXT_ID"
url = f"wss://sim-streaming.saxobank.com/sim/oapi/streaming/ws/connect?contextId={context_id}&authorization={token}"

ws = websocket.WebSocketApp(
    url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# ストリーミング開始
ws.run_forever()
```

**注意:**
WebSocket 接続を確立する前に、OpenAPI のエンドポイント（例: `root_services.subscriptions`）を使用してサブスクリプションを作成し、`ContextId` と `ReferenceId` を設定する必要があります。
