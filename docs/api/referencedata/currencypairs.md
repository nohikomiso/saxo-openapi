# ReferenceData - Currency Pairs

通貨ペアのデータを取得します。

## エンドポイント

### CurrencyPairs - 通貨ペア一覧取得

利用可能な通貨ペアのデータを取得します。

**エンドポイント:** `GET /openapi/ref/v1/currencypairs/`

**パラメータ:** なし

**レスポンス:**
- JSON Schema: [currency_pairs_response.json](../../schemas/referencedata/currencypairs/currency_pairs_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# 通貨ペア一覧を取得
r = rd.currencypairs.CurrencyPairs()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "Identifier": "EURUSD",
      "Symbol": "EUR/USD"
    },
    {
      "Identifier": "USDJPY",
      "Symbol": "USD/JPY"
    },
    {
      "Identifier": "GBPUSD",
      "Symbol": "GBP/USD"
    }
  ]
}
```

---

## 主要フィールド

- `Identifier`: 通貨ペア識別子
- `Symbol`: 通貨ペア記号

## ユースケース

- FX取引での通貨ペア選択
- 為替レート表示
- 通貨換算

## 関連エンドポイント

- [Currencies](./currencies.md) - 通貨参照データ
- [Instruments](./instruments.md) - 金融商品参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
