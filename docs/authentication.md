# 認証ガイド

Saxo OpenAPI を使用するための認証設定の詳細ガイド

## 認証の概要

Saxo OpenAPI は OAuth 2.0 を使用して認証を行います。API リクエストには、必ず有効な **アクセストークン** が必要です。

### 認証フロー

1. Saxo Developer Portal でアプリケーションを登録
2. OAuth 2.0 フローを使用してアクセストークンを取得
3. アクセストークンを API リクエストに含める
4. トークンの有効期限が切れたら、リフレッシュトークンで更新

## アクセストークンの取得

### 方法 1: Saxo Developer Portal (テスト用)

開発・テスト目的で簡単にトークンを取得する方法:

1. [Saxo Developer Portal](https://www.developer.saxo/) にログイン
2. **Applications** セクションに移動
3. アプリケーションを作成 (または既存のものを選択)
4. **OAuth2.0 Token** セクションで **Generate Token** をクリック
5. 生成されたアクセストークンをコピー

**注意**: Developer Portal で生成されたトークンの有効期限は通常 **20 分** です。

### 方法 2: OAuth 2.0 認証フロー (本番用)

本番環境では、完全な OAuth 2.0 認証フローを実装する必要があります:

1. **Authorization Code Grant** フローを使用
2. ユーザーを Saxo の認証ページにリダイレクト
3. 認証後、認可コードを取得
4. 認可コードをアクセストークンとリフレッシュトークンに交換

詳細は [Saxo OAuth Documentation](https://www.developer.saxo/openapi/learn/oauth-authorization-code-grant) を参照してください。

## トークンの安全な管理

### 環境変数の使用 (推奨)

トークンをソースコードに直接記述せず、環境変数から読み込みます:

```bash
# トークンを環境変数に設定
export SAXO_ACCESS_TOKEN="your_access_token_here"
```

Python コード:

```python
import os
from saxo_openapi import API

# 環境変数からトークンを読み込む
token = os.getenv("SAXO_ACCESS_TOKEN")
if not token:
    raise ValueError("SAXO_ACCESS_TOKEN environment variable not set")

client = API(access_token=token)
```

### .env ファイルの使用

開発環境では `.env` ファイルを使用すると便利です:

```bash
# .env ファイル (必ず .gitignore に追加)
SAXO_ACCESS_TOKEN=your_access_token_here
```

Python コード (`python-dotenv` を使用):

```python
from dotenv import load_dotenv
import os
from saxo_openapi import API

# .env ファイルを読み込む
load_dotenv()

token = os.getenv("SAXO_ACCESS_TOKEN")
client = API(access_token=token)
```

**重要**: `.env` ファイルは必ず `.gitignore` に追加し、Git リポジトリにコミットしないでください。

```gitignore
# .gitignore
.env
*.env
```

## リフレッシュトークンの使用

アクセストークンの有効期限は短い (通常 20 分) ため、長時間実行するアプリケーションではリフレッシュトークンを使用してトークンを更新する必要があります。

### リフレッシュトークンの取得

OAuth 2.0 認証フローを完了すると、アクセストークンと一緒にリフレッシュトークンが発行されます。

### トークンの更新

```python
import requests

def refresh_access_token(refresh_token, client_id, client_secret):
    """
    リフレッシュトークンを使用してアクセストークンを更新
    """
    token_url = "https://live.logonvalidation.net/token"
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    
    return response.json()["access_token"]
```

## セキュリティベストプラクティス

### 1. トークンをソースコードに含めない

```python
# ❌ 悪い例
token = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjhBRUE3..."
client = API(access_token=token)

# ✅ 良い例
import os
token = os.getenv("SAXO_ACCESS_TOKEN")
client = API(access_token=token)
```

### 2. トークンを安全に保存

- 環境変数、または暗号化されたストレージを使用
- ログやエラーメッセージにトークンを出力しない
- Git リポジトリにトークンをコミットしない

### 3. 適切な権限スコープを使用

OAuth 2.0 認証時に、必要最小限のスコープのみをリクエストします:

```python
# 例: 読み取り専用スコープ
scopes = ["openapi:trading:read", "openapi:portfolio:read"]
```

### 4. HTTPS を使用

本番環境では必ず HTTPS を使用してトークンを送信します (Saxo API はデフォルトで HTTPS)。

## トラブルシューティング

### エラー: `HTTP 401 Unauthorized`

**原因**:
- アクセストークンが無効または期限切れ
- トークンが正しく設定されていない

**解決策**:
1. トークンの有効期限を確認
2. 新しいトークンを取得
3. 環境変数が正しく設定されているか確認:
   ```bash
   echo $SAXO_ACCESS_TOKEN
   ```

### エラー: `HTTP 403 Forbidden`

**原因**:
- トークンに必要な権限スコープがない
- アカウントに API アクセス権限がない

**解決策**:
1. OAuth 認証時に適切なスコープをリクエスト
2. Saxo アカウントの API アクセス権限を確認

### トークンが頻繁に期限切れになる

**解決策**:
- リフレッシュトークンを使用して自動的にトークンを更新
- トークンの有効期限を監視し、期限切れ前に更新

```python
import time
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, access_token, expires_in=1200):
        self.access_token = access_token
        self.expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    def is_expired(self):
        # 1分のバッファを持たせる
        return datetime.now() >= (self.expires_at - timedelta(minutes=1))
    
    def get_token(self):
        if self.is_expired():
            # トークンを更新
            self.access_token = refresh_access_token(...)
            self.expires_at = datetime.now() + timedelta(seconds=1200)
        
        return self.access_token
```

## 参考資料

- [Saxo OAuth Documentation](https://www.developer.saxo/openapi/learn/oauth-authorization-code-grant)
- [Saxo Developer Portal](https://www.developer.saxo/)
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749)
