# ReferenceData - Exchanges

取引所に関する参照データを取得します。

## エンドポイント

### ExchangeList - 取引所一覧取得

取引所のリストを詳細情報とともに取得します。レスポンスには取引ステータスなど、関連データへのリンクも含まれます。

**エンドポイント:** `GET /openapi/ref/v1/exchanges/`

**パラメータ:**
- なし（オプションパラメータあり）

**レスポンス:**
- JSON Schema: [exchange_list_response.json](../../schemas/referencedata/exchanges/exchange_list_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# 取引所一覧を取得
r = rd.exchanges.ExchangeList()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "ExchangeId": "XNYS",
      "Name": "New York Stock Exchange",
      "CountryCode": "US"
    },
    {
      "ExchangeId": "XNAS",
      "Name": "NASDAQ",
      "CountryCode": "US"
    }
  ]
}
```

---

### ExchangeDetails - 特定取引所の詳細取得

特定の取引所の詳細情報を取得します。

**エンドポイント:** `GET /openapi/ref/v1/exchanges/{ExchangeId}`

**パスパラメータ:**
- `ExchangeId` (string, 必須): 取引所ID

**レスポンス:**
- JSON Schema: [exchange_details_response.json](../../schemas/referencedata/exchanges/exchange_details_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# 特定の取引所の詳細を取得
ExchangeId = "XNYS"
r = rd.exchanges.ExchangeDetails(ExchangeId=ExchangeId)
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "ExchangeId": "XNYS",
  "Name": "New York Stock Exchange",
  "CountryCode": "US",
  "TimeZone": "Eastern Standard Time"
}
```

---

## 主要フィールド

- `ExchangeId`: 取引所ID
- `Name`: 取引所名
- `CountryCode`: 国コード
- `TimeZone`: タイムゾーン

## ユースケース

- 取引所情報の表示
- 市場時間の確認
- 取引可能商品の検索

## 関連エンドポイント

- [Instruments](./instruments.md) - 金融商品参照データ
- [TimeZones](./timezones.md) - タイムゾーン参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
