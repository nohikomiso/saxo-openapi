# 認証ガイド

Saxo OpenAPI を使用するための認証設定と、最新のトークン管理機能の詳細ガイドです。

## 認証の概要

Saxo OpenAPI は OAuth 2.0 を使用して認証を行います。API リクエストには、必ず有効な **アクセストークン** が必要です。
アクセストークンの有効期限は短く（通常20分以内）、長時間稼働するアプリケーション（ボットなど）では定期的なリフレッシュが必要です。

このライブラリには、OAuth2.0のログインからトークン管理・自動リフレッシュまでを行う完全な機能が組み込まれています。外部ライブラリ（例: Saxo-APY）は必要ありません。

利用者のユースケースに合わせて、**2つのアプローチ**が用意されています。

---

## アプローチ 1: 組み込みの `SaxoAuthClient` を使用する（推奨）

この方法は、1つのPythonアプリケーション内でログインからトレードまで全てを完結させたい一般ユーザーに推奨されます。

### 特徴
- ローカルリダイレクトサーバーを内包し、ブラウザログインを自動化
- トークンが切れる前にバックグラウンドで自動リフレッシュ（非同期）
- APIクラスに直接注入することで、通信時に常に最新のトークンを使用可能
- トークン更新時に任意の関数を実行できる「コールバック機構」により、安全な保存処理を自由に記述可能

### 実装例

```python
import json
from saxo_api_client import API
from saxo_api_client.auth import SaxoAuthClient
import saxo_api_client.endpoints.portfolio as pf

# トークンがリフレッシュされた瞬間に呼ばれるコールバック（自由記述）
def save_token(token_data):
    # 例: 暗号化してファイルに保存、DBに保存など
    with open("token.json", "w") as f:
        json.dump(token_data.model_dump(), f)

# 1. 認証クライアントの初期化
# （app_config.json は Saxo Developer Portal から取得したアプリ設定）
auth = SaxoAuthClient(app_config="app_config.json", on_token_refresh=save_token)

# 2. ログイン処理（ブラウザが起動し、リダイレクトを待機）
auth.login(launch_browser=True, catch_redirect=True)

# 3. APIクライアントへ注入 (Dependency Injection)
# これにより、APIは常に auth の最新トークンを使って通信します
client = API(auth_client=auth)

# リクエスト例
r = pf.balances.AccountBalancesMe()
rv = client.request(r)
print(rv)
```

---

## アプローチ 2: アクセストークン（文字列）を直接注入する

この方法は、**認証専用のマイクロサービス**を別に立てており、そこから発行されたアクセストークン（文字列）を受け取ってAPIを実行したいだけのシステムに適しています。

### 特徴
- ライブラリ側での自動リフレッシュやファイル保存は一切行わない
- 完全なステートレス・疎結合

### 実装例

```python
import os
from saxo_api_client import API
import saxo_api_client.endpoints.portfolio as pf

# 外部から取得したトークン文字列
token = os.getenv("SAXO_ACCESS_TOKEN")
if not token:
    raise ValueError("SAXO_ACCESS_TOKEN environment variable not set")

# APIクライアントの初期化（文字列渡し）
# 既定は simulation ゲートウェイ。Live トークンは environment="live" を付ける
client = API(access_token=token, environment="live")

# または OAuth 保存 JSON から（ファイル名 / base_uri から推論）
# from saxo_api_client.contrib.client import SaxoClient
# client = SaxoClient.from_token_file("saxo_token_live_live.json")._api

r = pf.balances.AccountBalancesMe()
rv = client.request(r)
print(rv)
```

> [!WARNING]
> このアプローチでは自動リフレッシュが行われないため、トークンの有効期限（20分）が切れると `HTTP 401 Unauthorized` が発生します。トークンの更新・再設定は、呼び出し側のアプリケーション自身で責任を持って実装してください。

---

## トラブルシューティング

### エラー: `HTTP 401 Unauthorized`

**原因**:
- アクセストークンが無効または期限切れ
- `API(access_token="...")` で初期化したあと、新しいトークンを再設定せずに使い続けている
- **Live トークンなのに simulation ゲートウェイ**（`gateway.saxobank.com/sim/openapi/...`）へ送っている — `access_token` のみでは既定が simulation

**解決策**:
- Live: `environment="live"`、`SaxoClient.from_token_file(...)`、または `API(auth_client=...)`（`app_config` から LIVE/SIM を自動推論）
- アプローチ1の `auth_client` の直接注入に切り替えるか、トークン更新ロジックを見直してください。

### エラー: `HTTP 403 Forbidden`

**原因**:
- トークンに必要な権限スコープがない（例: トレードAPIを呼ぼうとしたがREADスコープのみ）
- Saxo Developer Portal 側でアプリの権限が不足している

**解決策**:
- OAuth 認証時のスコープを見直すか、Saxo Developer Portal でアプリの権限設定を確認してください。

## 参考資料
- [Saxo OAuth Documentation](https://www.developer.saxo/openapi/learn/oauth-authorization-code-grant)
- [Saxo Developer Portal](https://www.developer.saxo/)
