# ReferenceData - Languages

Saxo Bank がサポートする言語のリストを取得します。

## エンドポイント

### Languages - 言語一覧取得

Saxo Bank でサポートされているすべての言語のリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/languages/`

**パラメータ:** なし

**レスポンス:**
- JSON Schema: [languages_response.json](../../schemas/referencedata/languages/languages_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# サポートされている言語の一覧を取得
r = rd.languages.Languages()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "LanguageCode": "en",
      "Name": "English"
    },
    {
      "LanguageCode": "da",
      "Name": "Danish"
    },
    {
      "LanguageCode": "ja",
      "Name": "Japanese"
    }
  ]
}
```

---

## 主要フィールド

- `LanguageCode`: ISO 639-1 言語コード（2文字）
- `Name`: 言語名

## ユースケース

- UI言語設定の選択肢表示
- コンテンツのローカライゼーション
- ユーザープリファレンスの管理

## 関連エンドポイント

- [Cultures](./cultures.md) - カルチャー（言語・地域）参照データ
- [Countries](./countries.md) - 国コード参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
- [ISO 639 Language Codes](https://www.iso.org/iso-639-language-codes.html)
