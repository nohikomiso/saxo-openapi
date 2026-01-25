# ReferenceData - Currencies

Saxo Bank がサポートする通貨のリストを取得します。

## エンドポイント

### Currencies - 通貨一覧取得

サポートされているすべての通貨のリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/currencies/`

**パラメータ:** なし

**レスポンス:**
- JSON Schema: [currencies_response.json](../../schemas/referencedata/currencies/currencies_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# サポートされている通貨の一覧を取得
r = rd.currencies.Currencies()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "CurrencyCode": "USD",
      "Decimals": 2,
      "Name": "US Dollar",
      "Symbol": "$"
    },
    {
      "CurrencyCode": "EUR",
      "Decimals": 2,
      "Name": "Euro",
      "Symbol": "€"
    },
    {
      "CurrencyCode": "JPY",
      "Decimals": 0,
      "Name": "Japanese Yen",
      "Symbol": "¥"
    }
  ]
}
```

---

## 主要フィールド

- `CurrencyCode`: ISO 4217 通貨コード（3文字）
- `Name`: 通貨名
- `Decimals`: 小数点以下の桁数
- `Symbol`: 通貨記号

## ユースケース

- 通貨選択リストの表示
- 通貨換算計算
- 価格表示のフォーマット設定

## 関連エンドポイント

- [CurrencyPairs](./currencypairs.md) - 通貨ペア参照データ
- [Countries](./countries.md) - 国コード参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
- [ISO 4217 Currency Codes](https://www.iso.org/iso-4217-currency-codes.html)
