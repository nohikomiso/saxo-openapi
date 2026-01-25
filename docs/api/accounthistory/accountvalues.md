# accounthistory.accountvalues

`accounthistory` グループの `accountvalues` モジュールです。

## AccountSummary

指定されたクライアントの口座の「ロールアップされたパフォーマンス」を取得します。

`GET openapi/hist/v3/accountValues/{ClientKey}/`

### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| ClientKey | string | Yes | クライアントキー |
| params | dict | No | クエリパラメータ |

### 使用例

```python
import saxo_openapi
import saxo_openapi.endpoints.accounthistory as ah
import json

client = saxo_openapi.API(access_token=...)
ClientKey = 'Cf4xZWiYL6W1nMKpygBLLA=='
r = ah.accountvalues.AccountSummary(ClientKey=ClientKey)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### レスポンス

成功時のレスポンススキーマは以下を参照してください:
[Response Schema](../../schemas/accounthistory/accountvalues/account_summary_response.json)
