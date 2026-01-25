# EventNotificationServices カテゴリ

イベント通知サービスのためのエンドポイント群

## 概要

EventNotificationServices (ENS) カテゴリは、クライアントのアクティビティに関するイベント通知を購読・管理する機能を提供します。注文の執行、ポジションの変更、口座の更新などのイベントをリアルタイムで受信できます。

## 主なユースケース

- **注文アクティビティ監視**: 注文の状態変化を監視
- **イベント通知受信**: クライアントアクティビティのリアルタイム通知
- **アクティビティ履歴**: 過去のクライアントアクティビティの取得
- **WebSocket連携**: ストリーミング接続でのイベント受信

## モジュール一覧

### [clientactivities](clientactivities.md)

クライアントアクティビティのイベント通知を管理します。

- `CreateSubscriptionForClientEvents`: クライアントイベントの購読作成
- `GetClientActivities`: クライアントアクティビティの履歴取得
- `RemoveSubscription`: 購読の削除

**主な用途**: イベント通知購読、アクティビティ監視

**購読可能なイベント**:
- `OrderActivities`: 注文関連のアクティビティ
- `PositionActivities`: ポジション関連のアクティビティ
- その他のクライアントアクティビティ

---

## イベント購読の仕組み

ENSでは、WebSocket接続を通じてイベントをリアルタイムで受信します:

1. **購読作成**: `CreateSubscriptionForClientEvents` で購読を作成
2. **WebSocket接続**: ストリーミング接続を確立
3. **イベント受信**: 購読したイベントがリアルタイムで配信される
4. **購読削除**: 不要になった購読を削除

## 関連するワークフロー例

- [WebSocket ストリーミング](../../examples/websocket_streaming.md) - イベント受信の実装例

## 次のステップ

- [RootServices カテゴリ](../rootservices/README.md) - セッション管理・購読管理
- [Trading カテゴリ](../trading/README.md) - 注文発注
- [API 全体索引](../README.md) - 全カテゴリ一覧
