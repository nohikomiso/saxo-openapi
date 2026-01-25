# {ワークフロー名}

{ワークフローの簡単な説明}

## 前提条件

- 認証済みクライアント
- ...

## 手順

1. ステップ1
2. ステップ2

## コード例

```python
from saxo_openapi import API
import saxo_openapi.endpoints.portfolio as portfolio
import saxo_openapi.endpoints.trading as trading
import json

def {workflow_function}(client):
    # ステップ1
    ...
    
    # ステップ2
    ...

if __name__ == "__main__":
    token = "YOUR_TOKEN"
    client = API(access_token=token)
    {workflow_function}(client)
```

## 期待される出力

```json
{
  ...
}
```

## エラーハンドリング

- `SaxoSException` を処理...

## 関連エンドポイント

- [エンドポイント1](../api/{category}/{module}.md#endpoint-1)
