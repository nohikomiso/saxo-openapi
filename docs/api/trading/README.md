# Trading カテゴリ

取引実行のためのエンドポイント群

## 概要

Trading カテゴリは、注文の発注・変更・キャンセル、価格情報の取得、オプション取引など、実際の取引実行に関連する機能を提供します。これらのエンドポイントは、トレーディングアプリケーションの中核となる機能です。

## 主なユースケース

- **注文発注**: 成行注文、指値注文、逆指値注文などの発注
- **注文管理**: 既存注文の変更、キャンセル
- **価格監視**: リアルタイム価格情報の取得とサブスクリプション
- **オプション取引**: オプションチェーンの取得と分析

## モジュール一覧

### [orders](orders.md) 👍 高優先度

注文の発注、変更、キャンセルを行います。

- `Order`: 新規注文の発注 (POST)
- `ChangeOrder`: 既存注文の変更 (PATCH)
- `CancelOrders`: 注文のキャンセル (DELETE)
- `PrecheckOrder`: 注文のプリチェック (発注前検証)

**主な用途**: 注文発注、注文管理

**ヘルパークラス**: [contrib/orders](../../contrib/orders.md) で注文作成を簡素化できます。

---

### [prices](prices.md) 👍 高優先度

価格情報の取得とリアルタイム価格サブスクリプションを提供します。

- `CreatePriceSubscription`: 価格のサブスクリプション作成
- `MarginImpactRequest`: マージンインパクトのリクエスト
- `PriceSubscriptionRemoveByTag`: サブスクリプション削除 (タグ指定)
- `PriceSubscriptionRemove`: サブスクリプション削除 (ID 指定)

**主な用途**: リアルタイム価格監視、価格アラート

---

### [infoprices](infoprices.md)

情報価格 (Info Prices) を取得します。

- `InfoPriceList`: 銘柄の情報価格一覧
- `InfoPriceSubscriptionCreate`: 情報価格のサブスクリプション作成
- サブスクリプション管理機能

**主な用途**: 取引前の価格情報確認

---

### [allocationkeys](allocationkeys.md)

アロケーションキー (注文の配分ルール) を管理します。

- `AllocationKeyDetails`: アロケーションキーの詳細取得
- `AllocationKeys`: アロケーションキー一覧

**主な用途**: 複数口座への注文配分

---

### [messages](messages.md)

取引メッセージを取得します。

- `Messages`: 取引関連のメッセージ一覧
- `MessageSubscriptionCreate`: メッセージサブスクリプション作成

**主な用途**: 取引通知、システムメッセージの確認

---

### [optionschain](optionschain.md)

オプションチェーン (オプション銘柄の一覧) を取得します。

- `OptionChain`: オプションチェーンの取得
- `OptionChainSubscription`: オプションチェーンのサブスクリプション

**主な用途**: オプション取引、オプション戦略の構築

---

### [positions](positions.md)

取引ポジションに関する情報を取得します。

**注意**: ポートフォリオのポジション監視には [portfolio/positions](../portfolio/positions.md) を使用してください。

- `Exercise`: オプションの行使
- `PositionDetails`: ポジション詳細

**主な用途**: オプション行使、ポジション詳細の確認

---

## 関連するワークフロー例

- [成行注文の発注](../../examples/place_market_order.md)
- [指値注文の発注](../../examples/place_limit_order.md)
- [注文のキャンセル](../../examples/cancel_orders.md)
- [WebSocket ストリーミング](../../examples/websocket_streaming.md) (価格とポジションのリアルタイム監視)

## Contrib モジュール

注文作成を簡素化するヘルパークラスが用意されています:

```python
from saxo_openapi.contrib.orders import (
    MarketOrder,
    LimitOrder,
    StopOrder,
    tie_account_to_order
)

# 成行注文の簡単な作成
order = MarketOrder(Uic=21, AssetType="FxSpot", Amount=10000)
```

詳細は [Contrib Orders ドキュメント](../../contrib/orders.md) をご覧ください。

## 次のステップ

- [Portfolio カテゴリ](../portfolio/README.md) - 残高・ポジション確認
- [ReferenceData カテゴリ](../referencedata/README.md) - 銘柄検索
- [API 全体索引](../README.md) - 全カテゴリ一覧
