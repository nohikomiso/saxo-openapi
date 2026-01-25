# Options Chain

## 概要

Options Chain（オプションチェーン）は、オプション契約の購読管理を行うエンドポイント群です。WebSocket経由でオプションチェーンデータのリアルタイム更新を受信する購読の作成・変更・削除・リセットを管理します。

## エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| OptionsChainSubscriptionCreate | POST | オプションチェーン購読を作成 |
| OptionsChainSubscriptionModify | PATCH | オプションチェーン購読を変更 |
| OptionsChainSubscriptionRemove | DELETE | オプションチェーン購読を削除 |
| OptionsChainSubscriptionResetATM | PUT | オプションチェーン購読をATMにリセット |

## OptionsChainSubscriptionCreate

アクティブなオプションチェーン購読を作成します。

### パラメータ

- **data** (dict, required): リクエストボディのパラメータ
  - Arguments: 購読対象のパラメータ（Uic, AssetType等）
  - ContextId: コンテキストID
  - ReferenceId: 参照ID
  - RefreshRate: 更新頻度（ミリ秒）

### JSON Schema

- **Body**: [options_chain_subscription_create_body.json](../../schemas/trading/optionschain/options_chain_subscription_create_body.json)
- **Response**: [options_chain_subscription_create_response.json](../../schemas/trading/optionschain/options_chain_subscription_create_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr
import json

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# オプションチェーン購読を作成
data = {
    "Arguments": {
        "Uic": 211,
        "AssetType": "StockOption"
    },
    "ContextId": "ctxt_20190316",
    "ReferenceId": "opt_01",
    "RefreshRate": 1000
}
r = tr.optionschain.OptionsChainSubscriptionCreate(data=data)
client.request(r)
print(json.dumps(r.response, indent=4))
```

## OptionsChainSubscriptionModify

既存のオプションチェーン購読を変更します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **ReferenceId** (string, required): 参照ID
- **data** (dict, required): 変更するパラメータ

### JSON Schema

- **Body**: [options_chain_subscription_modify_body.json](../../schemas/trading/optionschain/options_chain_subscription_modify_body.json)
- **Response**: [options_chain_subscription_modify_response.json](../../schemas/trading/optionschain/options_chain_subscription_modify_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# オプションチェーン購読を変更
ReferenceId = "opt_01"
ContextId = "ctxt_20190316"
data = {
    "Arguments": {
        "MinMoneyness": -0.5,
        "MaxMoneyness": 0.5
    }
}
r = tr.optionschain.OptionsChainSubscriptionModify(
    ReferenceId=ReferenceId,
    ContextId=ContextId,
    data=data)
client.request(r)
assert r.status_code == r.expected_status
```

## OptionsChainSubscriptionRemove

オプションチェーン購読を削除します。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **ReferenceId** (string, required): 参照ID

### JSON Schema

- **Response**: [options_chain_subscription_remove_response.json](../../schemas/trading/optionschain/options_chain_subscription_remove_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# オプションチェーン購読を削除
ReferenceId = "opt_01"
ContextId = "ctxt_20190316"
r = tr.optionschain.OptionsChainSubscriptionRemove(
    ReferenceId=ReferenceId,
    ContextId=ContextId)
client.request(r)
assert r.status_code == r.expected_status
```

## OptionsChainSubscriptionResetATM

オプションチェーン購読を'At The Money'（ATM）にリセットします。

### パラメータ

- **ContextId** (string, required): コンテキストID
- **ReferenceId** (string, required): 参照ID

### JSON Schema

- **Response**: [options_chain_subscription_reset_atm_response.json](../../schemas/trading/optionschain/options_chain_subscription_reset_atm_response.json)

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.trading as tr

# クライアント初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# オプションチェーン購読をATMにリセット
ReferenceId = "opt_01"
ContextId = "ctxt_20190316"
r = tr.optionschain.OptionsChainSubscriptionResetATM(
    ReferenceId=ReferenceId,
    ContextId=ContextId)
client.request(r)
assert r.status_code == r.expected_status
```

## 関連エンドポイント

- [Reference Data Instruments](../referencedata/instruments.md) - 商品情報
- [WebSocket Streaming](../../contrib/websocket.md) - WebSocketストリーミングガイド
