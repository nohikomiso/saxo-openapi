# ReferenceData - Cultures

Saxo Bank がサポートするカルチャー（言語と地域の組み合わせ）のリストを取得します。

## エンドポイント

### Cultures - カルチャー一覧取得

ユーザー設定のローカライゼーションのために Saxo Bank でサポートされているすべてのカルチャーのリストを取得します。

**エンドポイント:** `GET /openapi/ref/v1/cultures/`

**パラメータ:** なし

**レスポンス:**
- JSON Schema: [cultures_response.json](../../schemas/referencedata/cultures/cultures_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# サポートされているカルチャーの一覧を取得
r = rd.cultures.Cultures()
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Data": [
    {
      "CultureCode": "en-US",
      "Name": "English (United States)"
    },
    {
      "CultureCode": "da-DK",
      "Name": "Danish (Denmark)"
    },
    {
      "CultureCode": "ja-JP",
      "Name": "Japanese (Japan)"
    }
  ]
}
```

---

## 主要フィールド

- `CultureCode`: カルチャーコード（言語-地域、例: "en-US", "ja-JP"）
- `Name`: カルチャー名（言語名と地域名、例: "Japanese (Japan)"）

## ユースケース

- UI言語設定の選択肢表示
- 日付・時刻・数値フォーマットのローカライゼーション
- ユーザープリファレンスの保存

## 関連エンドポイント

- [Languages](./languages.md) - 言語参照データ
- [Countries](./countries.md) - 国コード参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
- [RFC 5646 - Language Tags](https://tools.ietf.org/html/rfc5646)
