# API リファレンス

saxo_openapi ライブラリの全エンドポイント索引

## 概要

saxo_openapi ライブラリは、Saxo Bank OpenAPI の **103+ エンドポイント** をカバーしています。このページでは、全 8 カテゴリの概要と各カテゴリへのリンクを提供します。

## カテゴリ一覧

### 高優先度 (頻繁に使用される機能)

#### [Portfolio](portfolio/README.md) 👍

**説明**: ポートフォリオ管理

**主な機能**:
- 残高確認 (`balances`)
- ポジション監視 (`positions`)
- 口座情報取得 (`accounts`)
- クローズ済みポジション履歴 (`closedpositions`)

**モジュール数**: 10

**主なユースケース**: 残高確認、ポジション監視、口座管理

---

#### [Trading](trading/README.md) 👍

**説明**: 取引実行

**主な機能**:
- 注文発注・管理 (`orders`)
- 価格情報取得 (`prices`)
- オプション取引 (`optionschain`)

**モジュール数**: 7

**主なユースケース**: 注文発注、価格監視、オプション取引

---

### 中優先度

#### [ReferenceData](referencedata/README.md)

**説明**: 参照データ

**主な機能**:
- 銘柄検索 (`instruments`)
- 通貨情報 (`currencies`)
- 取引所情報 (`exchanges`)

**モジュール数**: 10

**主なユースケース**: 銘柄検索、通貨・取引所情報の取得

---

#### [AccountHistory](accounthistory/README.md)

**説明**: 口座履歴

**主な機能**:
- 口座評価額履歴 (`accountvalues`)
- 過去のポジション (`historicalpositions`)
- パフォーマンス分析 (`performance`)

**モジュール数**: 3

**主なユースケース**: パフォーマンス分析、履歴データ取得

---

#### [Chart](chart/README.md)

**説明**: チャートデータ

**主な機能**:
- チャートデータ取得 (`charts`)
- チャートサブスクリプション

**モジュール数**: 1

**主なユースケース**: チャート表示、テクニカル分析

**ドキュメント**:
- [charts.md](chart/charts.md) - チャートデータエンドポイント

---

#### [EventNotificationServices](eventnotificationservices/README.md)

**説明**: イベント通知サービス

**主な機能**:
- クライアント活動通知 (`clientactivities`)
- イベントサブスクリプション

**モジュール数**: 1

**主なユースケース**: イベント監視、通知受信

**ドキュメント**:
- [clientactivities.md](eventnotificationservices/clientactivities.md) - クライアント活動エンドポイント

---

#### [ValueAdd](valueadd/README.md)

**説明**: 付加価値サービス

**主な機能**:
- 価格アラート (`pricealerts`)
- 通知設定

**モジュール数**: 1

**主なユースケース**: アラート管理、通知設定

**ドキュメント**:
- [pricealerts.md](valueadd/pricealerts.md) - 価格アラートエンドポイント

---

### 低優先度

#### [RootServices](rootservices/README.md)

**説明**: システムサービス

**主な機能**:
- セッション管理 (`sessions`)
- システム診断 (`diagnostics`)
- サブスクリプション管理 (`subscriptions`)

**モジュール数**: 5

**主なユースケース**: セッション管理、システム診断、リソース管理

---

## エンドポイント総数

| カテゴリ | モジュール数 | 主なエンドポイント数 | 優先度 |
|---------|-------------|---------------------|--------|
| **Portfolio** | 10 | 28+ | 高 |
| **Trading** | 7 | 15+ | 高 |
| **ReferenceData** | 10 | 20+ | 中 |
| **AccountHistory** | 3 | 3 | 中 |
| **RootServices** | 5 | 8+ | 低 |
| **Chart** | 1 | 5+ | 中 |
| **EventNotificationServices** | 1 | 3+ | 中 |
| **ValueAdd** | 1 | 7+ | 中 |
| **合計** | **38** | **103+** | - |

## エンドポイント検索のヒント

### 1. カテゴリから探す

上記のカテゴリ一覧から、目的に合ったカテゴリを選択してください。

### 2. ユースケースから探す

よくあるユースケース:

- **残高を確認したい** → [Portfolio/balances](portfolio/balances.md)
- **注文を発注したい** → [Trading/orders](trading/orders.md)
- **銘柄を検索したい** → [ReferenceData/instruments](referencedata/instruments.md)
- **価格を監視したい** → [Trading/prices](trading/prices.md)
- **ポジションを確認したい** → [Portfolio/positions](portfolio/positions.md)

### 3. AI ナビゲーションを活用

`.ai/index.json` ファイルには、全エンドポイントの構造化メタデータが含まれています。AI アシスタント (Claude Code など) を使用すると、効率的にエンドポイントを検索できます。

```json
{
  "metadata": {
    "total_endpoints": 103,
    "total_examples": 28
  },
  "categories": { ... },
  "use_cases": {
    "balance_check": [...],
    "order_placement": [...],
    ...
  },
  "endpoints": [...]
}
```

## ワークフロー例

実践的な使用例は [examples](../examples/) ディレクトリにあります:

- [残高確認](../examples/check_balance.md)
- [成行注文の発注](../examples/place_market_order.md)
- [ポジション監視](../examples/monitor_positions.md)
- [WebSocket ストリーミング](../examples/websocket_streaming.md)

## Contrib モジュール

注文作成やユーティリティ機能を簡素化するヘルパークラス:

- [Contrib Orders](../contrib/orders.md) - 注文ヘルパークラス
- [Contrib WebSocket](../contrib/websocket.md) - WebSocket ストリーミング
- [Contrib Utilities](../contrib/utilities.md) - ユーティリティ関数

## JSON Schema

すべてのエンドポイントのレスポンス例は JSON Schema として提供されています:

```
docs/schemas/
├── portfolio/
│   ├── balances/
│   │   ├── account_balances_me_response.json
│   │   └── ...
│   └── positions/
├── trading/
└── ...
```

詳細は [schemas ディレクトリ](../schemas/) を参照してください。

## 次のステップ

- **[トップページに戻る](../README.md)**: ライブラリ全体の概要
- **[クイックスタート](../quickstart.md)**: 5分チュートリアル
- **[認証ガイド](../authentication.md)**: 認証設定の詳細

## サポート

- **ドキュメントバグ報告**: GitHub Issues
- **API 仕様**: [Saxo OpenAPI Documentation](https://www.developer.saxo/openapi/learn)
