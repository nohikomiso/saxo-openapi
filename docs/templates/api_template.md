# {モジュール名}

{モジュールの説明}

## エンドポイント

### {エンドポイントクラス名}

{エンドポイントの説明}

- **URL**: `{url}`
- **メソッド**: `{method}`

#### リクエスト

**パラメータ**

| 名前 | 型 | 必須 | 説明 |
|------|------|----------|----------------|
| ...  | ...  | ...      | ...            |

**ボディ**

[リクエストボディスキーマ](../../schemas/{category}/{subcategory}/{endpoint}_body.json)

#### レスポンス

[レスポンススキーマ](../../schemas/{category}/{subcategory}/{endpoint}_response.json)

#### 実行例

```python
import saxo_openapi
import saxo_openapi.endpoints.{category} as {category}
import json

client = saxo_openapi.API(access_token=...)
r = {category}.{subcategory}.{EndpointClassName}(...)
client.request(r)
print(json.dumps(r.response, indent=2))
```
