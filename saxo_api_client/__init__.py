# サブモジュールをインポート
from . import contrib, endpoints
from .exceptions import OpenAPIError
from .client import API
from .environment import resolve_api_environment

# よく使われる定義（Enum）をトップレベルに露出
from .definitions.orders import AssetType, OrderType, OrderDurationType, Direction

# バージョン情報
__version__ = "1.2.0"

# APIを直接インポートできるようにする
__all__ = [
    "API",
    "OpenAPIError",
    "resolve_api_environment",
    "contrib",
    "endpoints",
    "AssetType",
    "OrderType",
    "OrderDurationType",
    "Direction",
]
