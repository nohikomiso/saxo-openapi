# ReferenceData - Standard Dates

標準日付（フォワードテナー日、FXオプション満期日など）に関する参照データを取得します。

## エンドポイント

### ForwardTenorDates - フォワードテナー日一覧取得

特定のUIC（銘柄コード）のフォワードテナー日のリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/standarddates/forwardtenor/{Uic}`

**パスパラメータ:**
- `Uic` (int, 必須): 銘柄のUICコード

**パラメータ:**
- JSON Schema: [forward_tenor_dates_params.json](../../schemas/referencedata/standarddates/forward_tenor_dates_params.json)

**レスポンス:**
- JSON Schema: [forward_tenor_dates_response.json](../../schemas/referencedata/standarddates/forward_tenor_dates_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# フォワードテナー日を取得
Uic = 22
params = {
    "AccountKey": "your_account_key"
}
r = rd.standarddates.ForwardTenorDates(Uic=Uic, params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "Date": "2025-01-22",
      "Tenor": "1M"
    },
    {
      "Date": "2025-04-22",
      "Tenor": "3M"
    }
  ]
}
```

---

### FXOptionExpiryDates - FXオプション満期日一覧取得

特定のUIC（銘柄コード）のFXオプション満期日のリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/standarddates/fxoptionexpiry/{Uic}`

**パスパラメータ:**
- `Uic` (int, 必須): 銘柄のUICコード

**レスポンス:**
- JSON Schema: [fx_option_expiry_dates_response.json](../../schemas/referencedata/standarddates/fx_option_expiry_dates_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# FXオプション満期日を取得
Uic = 22
r = rd.standarddates.FXOptionExpiryDates(Uic=Uic)
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "Date": "2025-01-31",
      "ExpiryType": "Monthly"
    },
    {
      "Date": "2025-02-28",
      "ExpiryType": "Monthly"
    }
  ]
}
```

---

## 主要フィールド

- `Date`: 日付（ISO 8601形式）
- `Tenor`: テナー（期間、例: "1M", "3M"）
- `ExpiryType`: 満期タイプ

## ユースケース

- フォワード取引の日付選択
- FXオプション満期日の確認
- 取引期間の計画

## 関連エンドポイント

- [Instruments](./instruments.md) - 金融商品参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
