# Saxo OpenAPI Library Samples

このディレクトリには、Saxo OpenAPI ライブラリの使用方法や機能検証を行うためのサンプルスクリプトが含まれています。
これらのスクリプトは、ライブラリの正しい使用方法を理解するためのリファレンス実装としても機能します。

## スクリプト一覧

| ファイル名 | タイプ | 説明 |
|---|---|---|
| **Core Trading & Lifecycle** | | |
| `verify_lifecycle_trading.py` | Req/Res | 注文の完全なライフサイクル（発注 → 詳細取得 → キャンセル）を検証します。 |
| `verify_cycle_trading_full.py` | Req/Res | 成行注文での完全な取引サイクル（発注 → ポジション確認 → クローズ）の実践的サンプルです。 |
| `verify_scenario_options_cfd.py` | Streaming | オプションおよびCFDの取引シナリオ（検索 → オプションチェーン取得(Sub) → 発注）を検証します。 |
| `verify_orders_live.py` | Req/Res | 様々な注文タイプ（指値、逆指値、ストップリミット）の実践的な発注サンプルです。 |
| `verify_orders_precheck.py` | Req/Res | 注文前の事前チェック（PreCheck）機能のサンプルです。 |
| **Account & Portfolio** | | |
| `verify_monitor_account.py` | Req/Res | 口座の証拠金状況や価格のリアルタイム監視機能を検証します。 |
| `verify_history_account.py` | Req/Res | 過去のパフォーマンス、ポジション履歴、口座残高推移の取得を検証します。 |
| `verify_portfolio_fx.py` | Req/Res | FXポートフォリオ（残高、ポジション、注文）の基本的な取得サンプルです。 |
| **Reference Data** | | |
| `verify_refdata_details.py` | Req/Res | 銘柄詳細、取引所、言語、タイムゾーンなどの包括的な参照データ取得を検証します。 |
| `verify_refdata_fx.py` | Req/Res | FXに関連する参照データ（通貨ペア等）の取得サンプルです。 |
| **System & Diagnostics** | | |
| `verify_session_diag.py` | Req/Res | セッション機能、診断エンドポイント、認証状態の確認を行います。 |
| `verify_api_breaking_changes.py` | Req/Res | APIのバージョン変更や破壊的変更（例: エンドポイントパス変更）への対応を検証します。 |
| `verify_diagnostics_perf.py` | Req/Res | API応答時間を計測し、ネットワークやキャッシュのパフォーマンスを診断します。 |

## 使用方法

スクリプトを実行するには、プロジェクトルートで `uv run` を使用してください。

```bash
# 例: 取引ライフサイクルの検証
uv run libs/saxo_openapi/samples/verify_lifecycle_trading.py
```

## 前提条件

- `.env` ファイルに有効な `SAXO_24H_TOKEN` が設定されていること。
- シミュレーション環境 (Sim) での実行を推奨します。
