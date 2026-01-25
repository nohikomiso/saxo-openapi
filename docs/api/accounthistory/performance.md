# accounthistory.performance

`accounthistory` グループの `performance` モジュールです。

## AccountPerformance

特定のアカウントのパフォーマンス指標のコレクションを取得します。
アカウントのパフォーマンスは、アカウント所有者のみが閲覧できる機密情報を返します。
必須フィールドは `ClientKey` と、`StandardPeriod` または `FromDate`/`ToDate` のいずれかです。

`GET openapi/hist/v3/perf/{ClientKey}`

### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| ClientKey | string | Yes | クライアントキー |
| params | dict | No | クエリパラメータ（**注**: Pythonレベルではoptionalですが、APIレベルでは`StandardPeriod` または `FromDate`/`ToDate` が必須です） |

**注意**: `params`を省略した場合、API実行時に400エラーが返されます。

### 使用例

```python
import saxo_openapi
import saxo_openapi.endpoints.accounthistory as ah
import json

client = saxo_openapi.API(access_token=...)
ClientKey = 'Cf4xZWiYL6W1nMKpygBLLA=='
params = {
    'FromDate': '2019-03-01',
    'ToDate': '2019-03-10'
}
r = ah.performance.AccountPerformance(ClientKey=ClientKey,
                                      params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### レスポンス

成功時のレスポンススキーマは以下を参照してください:
[Response Schema](../../schemas/accounthistory/performance/account_performance_response.json)
