# サブモジュールをインポート
from . import contrib, endpoints
from .exceptions import OpenAPIError
from .saxo_openapi import API

# バージョン情報
__version__ = "0.1.0"

# APIを直接インポートできるようにする
__all__ = ["API", "OpenAPIError", "contrib", "endpoints"]
