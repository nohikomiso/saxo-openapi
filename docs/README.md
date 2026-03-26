# saxo_openapi ライブラリ

Saxo Bank OpenAPI の Python クライアントライブラリ

## 概要

`saxo_openapi` は、Saxo Bank が提供する OpenAPI を Python から利用するためのクライアントライブラリです。このライブラリは **AI-First 設計** を採用しており、コードとドキュメントを完全に分離することで、高い保守性と AI アシスタントによる効率的なナビゲーションを実現しています。

### 主要機能

- **103+ エンドポイント**: ポートフォリオ管理、取引実行、参照データ取得など、幅広い機能をカバー
- **8つのカテゴリ**: Portfolio, Trading, ReferenceData, AccountHistory, RootServices, Chart, EventNotificationServices, ValueAdd
- **Contrib モジュール**: 注文作成を簡素化するヘルパークラス群 (`MarketOrder`, `LimitOrder`, `OptionTrader` など)
- **WebSocket Streaming**: リアルタイム価格配信とポジション更新
- **包括的なドキュメント**: 全エンドポイントの日本語ドキュメント、JSON Schema、実行可能なコード例
- **AI ナビゲーション**: `.ai/index.json` による構造化メタデータで効率的なエンドポイント検索

## インストール

**pip を使用する場合**
```bash
pip install git+https://github.com/nohikomiso/saxo-openapi.git
```

**uv を使用する場合**
```bash
uv add git+https://github.com/nohikomiso/saxo-openapi.git
```

## クイックスタート

最初の API リクエストを 5 分で実行する方法は [クイックスタートガイド](quickstart.md) をご覧ください。

## 認証

Saxo OpenAPI を使用するには、アクセストークンが必要です。詳細な認証設定方法は [認証ガイド](authentication.md) をご覧ください。

## ドキュメント構造

```
docs/
├── README.md              # このファイル
├── quickstart.md          # 5分チュートリアル
├── authentication.md      # 認証設定ガイド
│
├── api/                   # API リファレンス
│   ├── README.md          # API 全体索引
│   ├── portfolio/         # ポートフォリオ管理
│   ├── trading/           # 取引実行
│   ├── referencedata/     # 参照データ
│   ├── accounthistory/    # 口座履歴
│   └── rootservices/      # システムサービス
│
├── contrib/               # Contrib モジュールドキュメント
│   ├── orders.md          # 注文ヘルパークラス
│   ├── trader.md          # SaxoTrader (FX/Stock/CFD)
│   ├── option_trader.md   # OptionTrader & OptionFinder
│   ├── websocket.md       # WebSocket streaming
│   └── utilities.md       # ユーティリティ関数
│
├── examples/              # ワークフロー例
│   ├── check_balance.md
│   ├── place_market_order.md
│   ├── websocket_streaming.md
│   └── ...
│
└── schemas/               # JSON Schema (レスポンス例)
    ├── portfolio/
    ├── trading/
    └── ...
```

## カテゴリ別ドキュメント

### 高優先度 (よく使用される機能)

- **[Portfolio](api/portfolio/README.md)** - ポートフォリオ管理
  - 残高確認、ポジション監視、口座情報取得
- **[Trading](api/trading/README.md)** - 取引実行
  - 注文発注・管理、価格情報取得、オプション取引

### 中優先度

- **[ReferenceData](api/referencedata/README.md)** - 参照データ
  - 銘柄検索、通貨・取引所情報
- **[AccountHistory](api/accounthistory/README.md)** - 口座履歴
  - パフォーマンス分析、履歴データ取得
- **[Chart](api/chart/README.md)** - チャートデータ
- **[EventNotificationServices](api/eventnotificationservices/README.md)** - イベント通知
- **[ValueAdd](api/valueadd/README.md)** - 付加価値サービス

### 低優先度

- **[RootServices](api/rootservices/README.md)** - システムサービス
  - セッション管理、診断、サブスクリプション管理

## ワークフロー例

実践的な使用例:

- [残高確認](examples/check_balance.md)
- [成行注文の発注](examples/place_market_order.md)
- [ポジション監視](examples/monitor_positions.md)
- [WebSocket ストリーミング](examples/websocket_streaming.md)
- [デルタヘッジワークフロー](examples/delta_hedging_workflow.md)

## AI-First 設計について

このライブラリは、以下の原則に基づいて再設計されました:

1. **ドキュメント完全分離**: Python コードは純粋なロジックのみ、詳細な説明は外部 Markdown
2. **構造化メタデータ**: `.ai/index.json` による AI アシスタント最適化
3. **実行可能なコード例**: すべてのコード例が copy-paste で動作
4. **JSON Schema**: レスポンス構造を明確に定義 (プレースホルダーなし)

詳細は [MIGRATION.md](MIGRATION.md) をご覧ください。

## 開発者向け

### ドキュメントリンクの検証

ドキュメント内の内部リンクを検証するスクリプトが用意されています:

```bash
# ライブラリルートから実行
./scripts/validate_links.py

# または uv 経由で実行
uv run scripts/validate_links.py
```

このスクリプトは、ライブラリがどこにインストールされていても正しく動作し、すべての内部リンクが有効であることを確認します。

## サポート

### ドキュメント

- **ドキュメントバグ報告**: GitHub Issues

### Saxo 公式ドキュメント

- **[学習用ガイド](https://www.developer.saxo/openapi/learn)**: Saxo OpenAPI の学習用ドキュメント
- **[リファレンスマニュアル](https://www.developer.saxo/openapi/referencedocs)**: API エンドポイントの詳細リファレンス

### コミュニティリソース

- **[SaxoBank OpenAPI Docs (Markdown版)](https://github.com/nohikomiso/SaxoBank-OpenAPI-Docs)**: Saxo 公式ドキュメントの Markdown 化版 (学習用ガイド、リファレンスマニュアルを含む)

## ライセンス

MIT License
