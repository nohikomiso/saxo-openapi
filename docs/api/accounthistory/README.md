# AccountHistory カテゴリ

口座履歴データ取得のためのエンドポイント群

## 概要

AccountHistory カテゴリは、口座の評価額履歴、過去のポジション、パフォーマンスデータなど、口座の履歴情報を提供します。これらのエンドポイントは、パフォーマンス分析、レポート作成、履歴データの確認に使用されます。

## 主なユースケース

- **パフォーマンス分析**: 口座のパフォーマンス推移を確認
- **履歴データ取得**: 過去のポジション、口座評価額の取得
- **レポート作成**: 取引履歴、損益レポートの作成

## モジュール一覧

### [accountvalues](accountvalues.md)

口座評価額の履歴を取得します。

- `AccountSummary`: 口座サマリー情報 (評価額履歴を含む)

**主な用途**: 口座評価額の推移確認、資産推移のグラフ作成

**取得できるデータ**:
- 日次の口座評価額
- 現金残高の推移
- マージン使用率の履歴

---

### [historicalpositions](historicalpositions.md)

過去のポジション履歴を取得します。

- `HistoricalPositions`: 指定期間内のポジション履歴

**主な用途**: 過去の取引履歴、ポジション分析

**取得できるデータ**:
- 指定期間内に保有していたポジション
- 損益の推移
- 銘柄別のポジション履歴

**クエリパラメータ**:
- `FromDate`: 開始日
- `ToDate`: 終了日
- `ClientKey`: クライアントキー (必須)

---

### [performance](performance.md)

口座のパフォーマンスデータを取得します。

- `AccountPerformance`: 口座パフォーマンス情報

**主な用途**: パフォーマンス分析、投資成績の確認

**取得できるデータ**:
- 時間加重収益率 (Time-Weighted Return)
- 内部収益率 (Internal Rate of Return)
- ベンチマークとの比較

---

## よくある使い方

### 過去のポジション履歴を取得

```python
import saxo_openapi.endpoints.accounthistory as ah
from saxo_openapi import API

client = API(access_token="YOUR_TOKEN")

# 2024年1月1日から1月31日までのポジション履歴を取得
params = {
    "ClientKey": "YOUR_CLIENT_KEY",
    "FromDate": "2024-01-01",
    "ToDate": "2024-01-31"
}
r = ah.historicalpositions.HistoricalPositions(params=params)
rv = client.request(r)

# 結果を表示
for position in rv.get('Data', []):
    print(f"Account: {position['AccountId']}")
    print(f"Instrument: {position['DisplayAndFormat']['Description']}")
    print(f"Profit/Loss: {position['ClosedProfitLoss']}")
    print("---")
```

### 口座パフォーマンスを取得

```python
# 口座のパフォーマンスデータを取得
params = {
    "ClientKey": "YOUR_CLIENT_KEY",
    "AccountKey": "YOUR_ACCOUNT_KEY"
}
r = ah.performance.AccountPerformance(params=params)
rv = client.request(r)

print(f"Time-Weighted Return: {rv.get('TimeWeightedReturn')}")
print(f"Benchmark Return: {rv.get('BenchmarkReturn')}")
```

## 関連するワークフロー例

- パフォーマンス分析ワークフロー例 (予定)

## 注意事項

- **データ取得期間**: 各エンドポイントには取得可能な期間の制限があります。詳細は各モジュールのドキュメントを参照してください。
- **パラメータ**: `ClientKey` は多くのエンドポイントで必須です。
- **データ更新頻度**: 履歴データは通常、日次で更新されます。

## 次のステップ

- [Portfolio カテゴリ](../portfolio/README.md) - 現在の残高・ポジション確認
- [Trading カテゴリ](../trading/README.md) - 取引実行
- [API 全体索引](../README.md) - 全カテゴリ一覧
