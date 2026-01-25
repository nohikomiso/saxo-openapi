# RootServices カテゴリ

システムサービスのためのエンドポイント群

## 概要

RootServices カテゴリは、セッション管理、システム診断、機能確認、サブスクリプション管理など、API システム全体に関連する機能を提供します。これらのエンドポイントは、アプリケーションの初期化、システムステータスの確認、リソース管理に使用されます。

## 主なユースケース

- **セッション管理**: ユーザーセッションの作成と管理
- **システム診断**: API の稼働状況とパフォーマンスの確認
- **機能確認**: 利用可能な機能とアクセス権限の確認
- **サブスクリプション管理**: アクティブなサブスクリプションの一括管理

## モジュール一覧

### [diagnostics](diagnostics.md)

システムの診断情報を取得します。

- `GetSystemStatus`: システムステータスの取得

**主な用途**: システム稼働状況の確認、障害診断

---

### [features](features.md)

利用可能な機能とアクセス権限を確認します。

- `Features`: ユーザーに利用可能な機能の一覧

**主な用途**: 機能の有効/無効確認、アクセス権限の確認

**確認できる情報**:
- 利用可能な資産クラス (AssetTypes)
- 利用可能な注文タイプ
- API 機能の有効/無効

---

### [sessions](sessions.md)

ユーザーセッションを管理します。

- `ChangeSession`: セッション情報の変更
- `CreateSession`: 新しいセッションの作成 (通常は自動)

**主な用途**: セッション管理、タイムアウト設定

---

### [subscriptions](subscriptions.md)

アクティブなサブスクリプションを一括管理します。

- `GetActiveSubscriptions`: アクティブなサブスクリプション一覧
- `RemoveMultipleActiveSubscriptions`: 複数のサブスクリプションを一括削除

**主な用途**: リソース管理、サブスクリプションのクリーンアップ

**サブスクリプションの種類**:
- 価格サブスクリプション (`trading/prices`)
- ポジションサブスクリプション (`portfolio/positions`)
- 残高サブスクリプション (`portfolio/balances`)
- その他のリアルタイムデータサブスクリプション

---

### [user](user.md)

ユーザー情報を取得します。

- `User`: ログインユーザーの情報取得

**主な用途**: ユーザー情報の確認、ユーザー設定の取得

---

## よくある使い方

### システムステータスの確認

```python
import saxo_openapi.endpoints.rootservices as root
from saxo_openapi import API

client = API(access_token="YOUR_TOKEN")

# システムステータスを確認
r = root.diagnostics.GetSystemStatus()
rv = client.request(r)

print(f"Status: {rv.get('Status')}")
```

### 利用可能な機能を確認

```python
# ユーザーに利用可能な機能を取得
r = root.features.Features()
rv = client.request(r)

# 利用可能な資産クラスを表示
asset_types = rv.get('AvailableAssetTypes', [])
print(f"Available Asset Types: {', '.join(asset_types)}")
```

### アクティブなサブスクリプションの一括削除

```python
# すべてのアクティブなサブスクリプションを取得
r = root.subscriptions.GetActiveSubscriptions()
rv = client.request(r)

print(f"Active Subscriptions: {len(rv.get('Data', []))}")

# サブスクリプションを一括削除 (クリーンアップ)
params = {"Tag": "cleanup"}
r = root.subscriptions.RemoveMultipleActiveSubscriptions(params=params)
client.request(r)
```

## サブスクリプション管理のベストプラクティス

### 1. アプリケーション終了時のクリーンアップ

```python
# アプリケーション終了時に全サブスクリプションを削除
import atexit

def cleanup_subscriptions():
    r = root.subscriptions.RemoveMultipleActiveSubscriptions()
    client.request(r)

atexit.register(cleanup_subscriptions)
```

### 2. 定期的なサブスクリプション確認

```python
import time

while True:
    # アクティブなサブスクリプション数を確認
    r = root.subscriptions.GetActiveSubscriptions()
    rv = client.request(r)
    
    active_count = len(rv.get('Data', []))
    print(f"Active Subscriptions: {active_count}")
    
    # 上限に近づいたらクリーンアップ
    if active_count > 50:
        cleanup_subscriptions()
    
    time.sleep(60)  # 1分ごとに確認
```

## 関連するワークフロー例

現在、RootServices カテゴリ専用のワークフロー例はありませんが、他のワークフローでサブスクリプション管理が使用されています:

- [WebSocket ストリーミング](../../examples/websocket_streaming.md) - サブスクリプション作成と削除

## 注意事項

- **サブスクリプション上限**: 同時にアクティブにできるサブスクリプション数には上限があります。不要なサブスクリプションは削除してください。
- **セッション管理**: セッションは通常自動的に管理されます。手動でのセッション管理は特殊なケースでのみ必要です。

## 次のステップ

- [Portfolio カテゴリ](../portfolio/README.md) - 残高・ポジション確認
- [Trading カテゴリ](../trading/README.md) - 取引実行
- [API 全体索引](../README.md) - 全カテゴリ一覧
