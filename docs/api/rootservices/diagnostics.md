# RootServices - Diagnostics

## 概要

Diagnosticsエンドポイントは、Saxo Bank OpenAPIの接続性をテストするためのエンドポイント群です。各HTTPメソッド（GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS）に対応したエンドポイントが用意されており、API接続の検証やデバッグに使用できます。

## エンドポイント一覧

| エンドポイント | HTTPメソッド | 説明 |
|--------------|------------|------|
| Get | GET | GETリクエストを送信し、200 OKレスポンスを受け取る |
| Post | POST | POSTリクエストを送信し、200 OKレスポンスを受け取る |
| Put | PUT | PUTリクエストを送信し、200 OKレスポンスを受け取る |
| Delete | DELETE | DELETEリクエストを送信し、200 OKレスポンスを受け取る |
| Patch | PATCH | PATCHリクエストを送信し、200 OKレスポンスを受け取る |
| Head | HEAD | HEADリクエストを送信し、200 OKレスポンスを受け取る |
| Options | OPTIONS | OPTIONSリクエストを送信し、200 OKレスポンスを受け取る |
| Echo | GET | リクエストの詳細（verb, url, headers, body）をレスポンスボディに含めて返す |

## クイック例

### 基本的な接続テスト

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

# APIクライアントの初期化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# GETリクエストのテスト
request = rs.diagnostics.Get()
response = client.request(request)
assert request.status_code == request.expected_status
print("GET test passed!")
```

### Echoエンドポイントでリクエストの確認

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエスト情報を取得
request = rs.diagnostics.Echo()
response = client.request(request)
print(f"Request details: {response}")
```

## 詳細仕様

### Get

**説明**: GETリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: GET  
**エンドポイント**: `/openapi/root/v1/diagnostics/get/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Get()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Post

**説明**: POSTリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: POST  
**エンドポイント**: `/openapi/root/v1/diagnostics/post/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Post()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Put

**説明**: PUTリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: PUT  
**エンドポイント**: `/openapi/root/v1/diagnostics/put/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Put()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Delete

**説明**: DELETEリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: DELETE  
**エンドポイント**: `/openapi/root/v1/diagnostics/delete/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Delete()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Patch

**説明**: PATCHリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: PATCH  
**エンドポイント**: `/openapi/root/v1/diagnostics/patch/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Patch()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Head

**説明**: HEADリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: HEAD  
**エンドポイント**: `/openapi/root/v1/diagnostics/head/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Head()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Options

**説明**: OPTIONSリクエストを送信し、200 OKレスポンスを受け取ります。

**HTTPメソッド**: OPTIONS  
**エンドポイント**: `/openapi/root/v1/diagnostics/options/`

**パラメータ**: なし

**レスポンス**: データは返されません

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Options()
rv = client.request(r)
assert r.status_code == r.expected_status
```

---

### Echo

**説明**: 任意のリクエストを送信し、リクエストの詳細（verb, url, headers, body）をレスポンスボディに含めて200 OKレスポンスを受け取ります。

**HTTPメソッド**: GET  
**エンドポイント**: `/openapi/root/v1/diagnostics/echo/`

**パラメータ**: なし

**レスポンス**: リクエストの詳細情報が返されます

**使用例**:

```python
import saxo_openapi
import saxo_openapi.endpoints.rootservices as rs

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
r = rs.diagnostics.Echo()
rv = client.request(r)
print(f"Echo response: {rv}")
```

## ユースケース

- **接続テスト**: API接続が正常に機能しているか確認
- **デバッグ**: リクエストの詳細情報を確認（Echoエンドポイント）
- **HTTPメソッドのサポート確認**: 特定のHTTPメソッドが正しく動作するか検証

## 関連ドキュメント

- [RootServices概要](./README.md)
- [Features](./features.md)
- [Sessions](./sessions.md)
