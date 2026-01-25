"""Saxo OpenAPI 型定義パッケージ

このパッケージは、Saxo OpenAPI でよく使用される主要な型定義を提供します。
型ヒントにより、AIコード生成時のエラーを削減し、IDE補完を改善します。

## 使用例

```python
from saxo_openapi.types import Uic, ClientKey, BalanceResponse

# プリミティブ型
uic: Uic = Uic(21)  # EUR/USD
client_key: ClientKey = ClientKey("Cf4xZWiYL6W1nMKpygBLLA==")

# レスポンス型
balance: BalanceResponse = {
    "CashBalance": 999956.74,
    "Currency": "EUR",
    "TotalValue": 996386.01,
}
```

See: docs/api/README.md
"""

from saxo_openapi.types.primitives import (
    AccountKey,
    AssetType,
    ClientKey,
    OrderId,
    PositionId,
    Uic,
)
from saxo_openapi.types.responses import (
    BalanceResponse,
    OrderResponse,
    PositionBaseResponse,
    PositionResponse,
    PositionViewResponse,
)

__all__ = [
    # Primitives
    "AccountKey",
    "AssetType",
    "ClientKey",
    "OrderId",
    "PositionId",
    "Uic",
    # Responses
    "BalanceResponse",
    "OrderResponse",
    "PositionBaseResponse",
    "PositionResponse",
    "PositionViewResponse",
]
