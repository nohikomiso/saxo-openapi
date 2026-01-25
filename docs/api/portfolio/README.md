# Portfolio カテゴリ

ポートフォリオ管理のためのエンドポイント群

## 概要

Portfolio カテゴリは、口座の残高、ポジション、注文履歴、口座情報など、ポートフォリオ管理に関連する機能を提供します。これらのエンドポイントは、トレーディングアプリケーションで最も頻繁に使用される機能です。

## 主なユースケース

- **残高確認**: 口座の現金残高、証拠金、取引可能額の確認
- **ポジション監視**: 現在保有しているポジションのリアルタイム監視
- **口座管理**: 口座情報の取得と更新
- **履歴データ**: クローズ済みポジション、過去の注文履歴の確認

## モジュール一覧

### [balances](balances.md) 👍 高優先度

口座の残高とマージン情報を取得します。

- `AccountBalancesMe`: ログインユーザーの残高取得
- `AccountBalances`: 特定の口座・グループの残高取得
- `MarginOverview`: マージン (証拠金) 概要
- サブスクリプション機能: リアルタイム残高更新

**主な用途**: 残高確認、証拠金監視

---

### [positions](positions.md) 👍 高優先度

現在保有しているポジション情報を取得します。

- `PositionsMe`: ログインユーザーのポジション一覧
- `PositionsQuery`: 条件指定でポジション検索
- `SinglePosition`: 個別ポジションの詳細
- サブスクリプション機能: リアルタイムポジション更新

**主な用途**: ポジション監視、損益確認

---

### [orders](orders.md)

ポートフォリオ内の注文履歴を取得します。

**注意**: 新規注文の発注は [trading/orders](../trading/orders.md) を使用してください。

- `OrdersMe`: ログインユーザーの注文一覧
- 注文ステータス: Active, Filled, Cancelled など

**主な用途**: 注文履歴の確認

---

### [accounts](accounts.md) 👍 高優先度

口座の詳細情報を取得・更新します。

- `AccountsMe`: ログインユーザーの全口座一覧
- `AccountDetails`: 特定の口座の詳細情報
- `AccountUpdate`: 口座設定の更新
- サブスクリプション機能: 口座情報のリアルタイム更新

**主な用途**: 口座情報の取得と管理

---

### [clients](clients.md)

クライアント情報を取得・更新します。

- `ClientDetailsMe`: ログインユーザーのクライアント情報
- `ClientDetails`: 特定のクライアント詳細
- `ClientDetailsUpdate`: クライアント設定の更新
- `ClientSwitchPosNettingMode`: ポジションネッティングモードの切替

**主な用途**: クライアント設定の管理

---

### [closedpositions](closedpositions.md)

クローズ済みのポジション履歴を取得します。

- `ClosedPositionsMe`: ログインユーザーのクローズ済みポジション
- `ClosedPositions`: 条件指定でクローズ済みポジション検索
- サブスクリプション機能: クローズ済みポジションのリアルタイム更新

**主な用途**: 過去の取引履歴、損益分析

---

### [exposure](exposure.md)

通貨エクスポージャー、資産クラス別のエクスポージャー情報を取得します。

- `ExposureCurrency`: 通貨別エクスポージャー
- `ExposureInstruments`: 銘柄別エクスポージャー
- `ExposureFxSpot`: FX スポットエクスポージャー

**主な用途**: リスク管理、エクスポージャー分析

---

### [netpositions](netpositions.md)

ネットポジション (複数ポジションを統合した純ポジション) を取得します。

- `NetPositionsMe`: ログインユーザーのネットポジション
- `NetPositions`: 条件指定でネットポジション検索
- サブスクリプション機能: ネットポジションのリアルタイム更新

**主な用途**: ポートフォリオ全体の純ポジション確認

---

### [users](users.md)

ユーザー情報を取得・更新します。

- `UsersMe`: ログインユーザーの情報取得
- `UserUpdate`: ユーザー設定の更新

**主な用途**: ユーザー設定の管理

---

### [accountgroups](accountgroups.md)

口座グループ情報を取得・管理します。

- `AccountGroupsMe`: ログインユーザーの口座グループ一覧
- `AccountGroupDetails`: 口座グループの詳細
- `AccountGroupUpdate`: 口座グループ設定の更新

**主な用途**: 複数口座のグループ管理

---

## 関連するワークフロー例

- [残高確認](../../examples/check_balance.md)
- [ポジション監視](../../examples/monitor_positions.md)
- [証拠金監視](../../examples/margin_monitoring.md)

## 次のステップ

- [Trading カテゴリ](../trading/README.md) - 注文発注・価格情報
- [ReferenceData カテゴリ](../referencedata/README.md) - 銘柄検索・通貨情報
- [API 全体索引](../README.md) - 全カテゴリ一覧
