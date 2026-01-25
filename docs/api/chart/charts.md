# Chart Services

このセクションでは、チャートデータの取得と購読を管理するためのエンドポイントを扱います。

---

## `GetChartData`

リクエストパラメータで指定されたチャートデータを返します。

### エンドポイント

`GET openapi/chart/v3/charts`

### パラメータ

| 名前      | 位置 | 説明                                                                    |
|-----------|------|-------------------------------------------------------------------------|
| AccountKey | query | データを取得するアカウントのキー。                                         |
| AssetType | query | チャートデータを取得する資産の種類（例: `Stock`, `FxSpot`）。             |
| Horizon   | query | チャートデータの時間軸（例: `1 minute`, `1 hour`, `1 day`）。            |
| Uic       | query | チャートデータを取得する銘柄のUic。                                       |
| Count     | query | 取得するバーの数。                                                      |
| FromDate  | query | データを取得する開始日時 (ISO 8601形式)。                               |
| ToDate    | query | データを取得する終了日時 (ISO 8601形式)。                               |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.chart as chart
import json
from datetime import datetime, timedelta

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストパラメータ
params = {
    "AccountKey": "Cf4xZ4v1q2fI5d5b7a3E7f==",  # 実際のアカウントキーに置き換える
    "AssetType": "Stock",
    "Horizon": "1 hour",
    "Uic": 211,  # 例: Apple Inc.のUic
    "Count": 100,
    "ToDate": datetime.now().isoformat()
}

# リクエストの作成と実行
r = chart.charts.GetChartData(params=params)
rv = client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# レスポンスボディの表示
print(json.dumps(rv, indent=2))
```

### レスポンス例

```json
{
  "Data": [
    {
      "Time": "2025-11-23T09:00:00.0000000Z",
      "Open": 150.00,
      "High": 151.20,
      "Low": 149.80,
      "Close": 151.00,
      "Volume": 100000
    },
    {
      "Time": "2025-11-23T10:00:00.0000000Z",
      "Open": 151.00,
      "High": 152.50,
      "Low": 150.90,
      "Close": 152.30,
      "Volume": 120000
    }
  ],
  "__VIEWSTATE": "..."
}
```

---

## `CreateChartDataSubscription`

購読を設定し、リクエストパラメータで指定された最も最近完了したサンプルの初期スナップショットを返します。
その後のサンプルはストリーミングチャネル経由で配信されます。通常、単一の新しいサンプルまたはサンプル更新が一度に配信されますが、サンプルがクローズすると、通常は2つのサンプル（クローズしたバーと新しく開いたバー）が配信されます。

### エンドポイント

`POST openapi/chart/v3/charts/subscriptions`

### ヘッダー

`Content-Type: application/json`

### リクエストボディ (`data`)

| 名前      | タイプ   | 説明                                                                    |
|-----------|----------|-------------------------------------------------------------------------|
| Uic       | integer  | チャートデータを購読する銘柄のUic。                                       |
| AssetType | string   | チャートデータを購読する資産の種類（例: `Stock`, `FxSpot`）。             |
| Horizon   | string   | チャートデータの時間軸（例: `1 minute`, `1 hour`, `1 day`）。            |
| FieldGroups | array of string | 購読するデータフィールドのグループ（例: `Chart`）。                 |
| ContextId | string   | 購読のコンテキストID。                                                  |
| ReferenceId | string | この購読の参照ID。                                                      |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.chart as ch
import json

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# リクエストボディのデータ
data = {
    "Uic": 211,  # 例: Apple Inc.のUic
    "AssetType": "Stock",
    "Horizon": "1 hour",
    "FieldGroups": ["Chart"],
    "ContextId": "my_chart_context",
    "ReferenceId": "my_chart_data_sub"
}

# リクエストの作成と実行
r = ch.charts.CreateChartDataSubscription(data=data)
rv = client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# レスポンスボディの表示
print(json.dumps(rv, indent=2))
```

### レスポンス例

```json
{
  "ContextId": "my_chart_context",
  "ReferenceId": "my_chart_data_sub",
  "Snapshot": {
    "Data": [
      {
        "Time": "2025-11-23T09:00:00.0000000Z",
        "Open": 150.00,
        "High": 151.20,
        "Low": 149.80,
        "Close": 151.00,
        "Volume": 100000
      }
    ],
    "__VIEWSTATE": "..."
  }
}
```

---

## `ChartDataRemoveSubscriptions`

現在のセッションでこのリソースのすべての購読を削除し、サーバー上のすべてのリソースを解放します。

### エンドポイント

`DELETE openapi/chart/v3/charts/subscriptions/{ContextId}`

### パラメータ

| 名前      | 位置 | 説明                                                                    |
|-----------|------|-------------------------------------------------------------------------|
| ContextId | path | 購読を削除する対象のコンテキストID。                                       |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.chart as ch

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 削除するContextIdを指定
ContextId = "my_chart_context"

# リクエストの作成と実行
r = ch.charts.ChartDataRemoveSubscriptions(ContextId=ContextId)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `202 Accepted` を返しますが、レスポンスボディにデータは含まれません。

---

## `ChartDataRemoveSubscription`

このリソース上で指定された参照IDの購読を削除し、サーバー上のリソースを解放します。

### エンドポイント

`DELETE openapi/chart/v3/charts/subscriptions/{ContextId}/{ReferenceId}`

### パラメータ

| 名前        | 位置 | 説明                                           |
|-------------|------|------------------------------------------------|
| ContextId   | path | 購読のコンテキストID。                         |
| ReferenceId | path | 削除する購読の参照ID。                         |

### コード例

```python
import saxo_openapi
import saxo_openapi.endpoints.chart as ch

# clientのインスタンス化
client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")

# 削除するContextIdとReferenceIdを指定
ContextId = "my_chart_context"
ReferenceId = "my_chart_data_sub"

# リクエストの作成と実行
r = ch.charts.ChartDataRemoveSubscription(ContextId=ContextId, ReferenceId=ReferenceId)
client.request(r)

# レスポンスの確認
print(f"ステータスコード: {r.status_code}")
assert r.status_code == r.expected_status

# このエンドポイントはデータを返しません
```

### レスポンス

このエンドポイントは成功時に `202 Accepted` を返しますが、レスポンスボディにデータは含まれません。
