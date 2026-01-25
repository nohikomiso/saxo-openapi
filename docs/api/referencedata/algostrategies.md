# ReferenceData - AlgoStrategies

アルゴリズム取引戦略に関する参照データを取得します。

## エンドポイント

### AlgoStrategies - アルゴリズム戦略一覧取得

利用可能なアルゴリズム戦略のリストを詳細情報とともに取得します。レスポンスにはパラメータなど、関連データへのリンクも含まれます。

**エンドポイント:** `GET /openapi/ref/v1/algostrategies/`

**パラメータ:**
- JSON Schema: [algo_strategies_params.json](../../schemas/referencedata/algostrategies/algo_strategies_params.json)

**レスポンス:**
- JSON Schema: [algo_strategies_response.json](../../schemas/referencedata/algostrategies/algo_strategies_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# ページネーションパラメータを指定
params = {
    "$top": 10,
    "$skip": 0
}

# アルゴリズム戦略一覧を取得
r = rd.algostrategies.AlgoStrategies(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "__count": 4,
  "Data": [
    {
      "Description": "Group of VWAP",
      "MinAmountUSD": 0,
      "Name": "VWAP",
      "Parameters": [],
      "SupportedDurationTypes": ["DayOrder"],
      "TradableInstrumentTypes": []
    },
    {
      "Description": "Groups of Iceberg Strategies",
      "MinAmountUSD": 0,
      "Name": "Iceberg",
      "Parameters": [],
      "SupportedDurationTypes": ["DayOrder"],
      "TradableInstrumentTypes": []
    }
  ]
}
```

---

### AlgoStrategyDetails - 特定アルゴリズム戦略の詳細取得

特定のアルゴリズム戦略の詳細情報を取得します。

**エンドポイント:** `GET /openapi/ref/v1/algostrategies/{Name}`

**パスパラメータ:**
- `Name` (string, 必須): 戦略名

**レスポンス:**
- JSON Schema: [algo_strategy_details_response.json](../../schemas/referencedata/algostrategies/algo_strategy_details_response.json)

**使用例:**

```python
import json
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd

client = saxo_openapi.API(access_token=...)

# 特定のアルゴリズム戦略の詳細を取得
Name = "Implementation Shortfall"
r = rd.algostrategies.AlgoStrategyDetails(Name=Name)
client.request(r)
print(json.dumps(r.response, indent=2))
```

**レスポンス例:**

```json
{
  "Description": "Group of IS strategies",
  "MinAmountUSD": 0,
  "Name": "Implementation Shortfall",
  "Parameters": [],
  "SupportedDurationTypes": ["DayOrder"],
  "TradableInstrumentTypes": []
}
```

---

## 主要フィールド

- `Name`: 戦略名
- `Description`: 戦略の説明
- `MinAmountUSD`: 最小取引金額（USD）
- `Parameters`: 戦略パラメータのリスト
- `SupportedDurationTypes`: サポートされる注文期間タイプ
- `TradableInstrumentTypes`: 取引可能な商品タイプ

## 関連エンドポイント

- [Instruments](./instruments.md) - 金融商品参照データ

## 参考リンク

- [Saxo Bank OpenAPI リファレンス](https://www.developer.saxo/)
