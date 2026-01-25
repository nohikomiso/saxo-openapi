# Trade Messages

## 概要

Trade Messages（取引メッセージ）は、取引に関するメッセージの取得・管理・購読を行うエンドポイント群です。取引実行時の確認メッセージやアラートなどを処理します。

## エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| GetTradeMessages | GET | 現在のユーザーの取引メッセージを取得 |
| MarkMessageAsSeen | PUT | メッセージを既読としてマーク |
| CreateTradeMessageSubscription | POST | 取引メッセージのWebSocket購読を作成 |
| RemoveTradeMessageSubscriptionById | DELETE | IDによる取引メッセージ購読を削除 |
| RemoveTradeMessageSubscriptions | DELETE | 複数の取引メッセージ購読を削除 |

## GetTradeMessages

現在のユーザーに対する取引メッセージを取得します。

### パラメータ

なし

### JSON Schema

- **Response**: [get_trade_messages_response.json](../../schemas/trading/messages/get_trade_messages_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 取引メッセージを取得
r = tr.messages.GetTradeMessages()
client.request(r)
print(json.dumps(r.response, indent=4))
```

## MarkMessageAsSeen

メッセージを既読としてマークします。論理的には、メッセージを「既読」コレクションに移動することで実現されます。

### パラメータ

- **MessageId** (string, required): メッセージID

### JSON Schema

- **Response**: [mark_message_as_seen_response.json](../../schemas/trading/messages/mark_message_as_seen_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# メッセージを既読にマーク
MessageId = "MESSAGE_ID_HERE"
r = tr.messages.MarkMessageAsSeen(MessageId=MessageId)
client.request(r)
assert r.status_code == r.expected_status
```

## CreateTradeMessageSubscription

WebSocket経由で取引メッセージのリアルタイム更新を受信する購読を作成します。

### パラメータ

- **data** (dict, required): リクエストボディのパラメータ
  - ContextId: コンテキストID
  - ReferenceId: 参照ID

### JSON Schema

- **Body**: [create_trade_message_subscription_body.json](../../schemas/trading/messages/create_trade_message_subscription_body.json)
- **Response**: [create_trade_message_subscription_response.json](../../schemas/trading/messages/create_trade_message_subscription_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 取引メッセージ購読を作成
data = {
    "ContextId": "ctxt_20190317",
    "ReferenceId": "msg_01"
}
r = tr.messages.CreateTradeMessageSubscription(data=data)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## RemoveTradeMessageSubscriptionById

IDを指定して、単一の取引メッセージ購読を削除します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **ReferenceId** (string, required): 参照ID

### JSON Schema

- **Response**: [remove_trade_message_subscription_by_id_response.json](../../schemas/trading/messages/remove_trade_message_subscription_by_id_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# IDによる取引メッセージ購読を削除
ContextId = "ctxt_20190317"
ReferenceId = "msg_01"
r = tr.messages.RemoveTradeMessageSubscriptionById(
    ContextId=ContextId,
    ReferenceId=ReferenceId)
client.request(r)
assert r.status_code == r.expected_status
```

## RemoveTradeMessageSubscriptions

コンテキストIDとタグを指定して、複数の取引メッセージ購読を削除します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **params** (dict, required): クエリパラメータ
  - Tag: 削除対象のタグ

### JSON Schema

- **Params**: [remove_trade_message_subscriptions_params.json](../../schemas/trading/messages/remove_trade_message_subscriptions_params.json)
- **Response**: [remove_trade_message_subscriptions_response.json](../../schemas/trading/messages/remove_trade_message_subscriptions_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 複数の取引メッセージ購読を削除
ContextId = "ctxt_20190317"
params = {"Tag": "MyTag"}
r = tr.messages.RemoveTradeMessageSubscriptions(
    ContextId=ContextId,
    params=params)
client.request(r)
assert r.status_code == r.expected_status
```

## 関連エンドポイント

- [Trading Orders](../trading/orders.md) - 注文関連エンドポイント
- [WebSocket Streaming](../../contrib/websocket.md) - WebSocketストリーミングガイド
