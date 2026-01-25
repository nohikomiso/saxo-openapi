# ReferenceData - Countries

Saxo Bank がサポートする国のリストを取得します。

## エンドポイント

### Countries - 国コード一覧取得

Saxo Bank でサポートされているすべての国のリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/countries/`

**パラメータ:** なし

**レスポンス:**
- JSON Schema: [countries_response.json](../../schemas/referencedata/countries/countries_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# サポートされている国の一覧を取得
r = rd.countries.Countries()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "A3": "AFG",
      "CountryCode": "AF",
      "Name": "Afghanistan",
      "Numeric": 4
    },
    {
      "A3": "ALA",
      "CountryCode": "AX",
      "Name": "Aland Islands",
      "Numeric": 248
    }
  ]
}
```

---

## 主要フィールド

- `CountryCode`: ISO 3166-1 alpha-2 国コード（2文字）
- `A3`: ISO 3166-1 alpha-3 国コード（3文字）
- `Name`: 国名
- `Numeric`: ISO 3166-1 数値国コード

## ユースケース

- アカウント開設時の国選択リスト
- 居住地・市民権の検証
- 地域別の規制要件確認

## 関連エンドポイント

- [Cultures](./cultures.md) - カルチャー（言語・地域）参照データ
- [Languages](./languages.md) - 言語参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
- [ISO 3166 Country Codes](https://www.iso.org/iso-3166-country-codes.html)
