# Root Services - User

このセクションでは、現在のユーザー情報を取得するためのエンドポイントを扱います。

---

## `User`

現在ログインしているユーザーの情報を取得します。

### エンドポイント

```
GET openapi/root/v1/user/
```

### パラメータ
このエンドポイントはパラメータを必要としません。

### コード例

```python
import saxo_openapi
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストの作成と実行
r = saxo_openapi.endpoints.rootservices.user.User()
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# レスポンスボディの表示
print(json.dumps(r.response, indent=2))
```

### レスポンス例

```json
{
  "ClientKey": "Cf4xZ4v1q2fI5d5b7a3E7f==",
  "Culture": "en-US",
  "Language": "en",
  "LastLoginStatus": "Successful",
  "LastLoginTime": "2025-11-23T10:30:00.123Z",
  "LegalAssetTypes": [
    "FxSpot",
    "FxForwards",
    "FxVanillaOption",
    "FxKnockInOption",
    "FxKnockOutOption"
  ],
  "MarketDataViaOpenApi": True,
  "Name": "John Doe",
  "PartnerPlatformId": "MyTradingApp",
  "TimeZoneId": 120,
  "UserId": "987654321"
}
```
