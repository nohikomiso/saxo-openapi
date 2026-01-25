# JSON Schemas

このディレクトリには、Saxo OpenAPI の全エンドポイントのJSON Schemaが含まれています。

## 概要

Phase 1で自動生成された239個のJSON Schemaファイルがカテゴリ別に整理されています:

- `portfolio/` - ポートフォリオ関連エンドポイント
- `trading/` - 取引関連エンドポイント
- `referencedata/` - 参照データエンドポイント
- `accounthistory/` - アカウント履歴エンドポイント
- `rootservices/` - ルートサービスエンドポイント
- `chart/` - チャートデータエンドポイント
- `eventnotificationservices/` - イベント通知エンドポイント
- `valueadd/` - 付加価値サービスエンドポイント

## ファイル命名規則

各エンドポイントには最大3種類のスキーマファイルが存在します:

### レスポンススキーマ（必須）

```
{endpoint}_response.json
```

エンドポイントのレスポンス構造を定義します。すべてのエンドポイントに存在します。

**例**: `account_balances_response.json`

### クエリパラメータスキーマ（オプション）

```
{endpoint}_params.json
```

エンドポイントのクエリパラメータを定義します。パラメータが存在するエンドポイントのみ。

**例**: `account_balances_params.json`

### リクエストボディスキーマ（オプション）

```
{endpoint}_body.json
```

POST/PUT/PATCHリクエストのボディ構造を定義します。ボディが必要なエンドポイントのみ。

**例**: `order_body.json`

## 空パラメータファイル

以下の18個のエンドポイントはクエリパラメータが不要なため、`{}` (空オブジェクト) となっています:

```
accounthistory/accountvalues/account_summary_params.json
chart/charts/chart_data_remove_subscription_params.json
chart/charts/chart_data_remove_subscriptions_params.json
chart/charts/create_chart_data_subscription_params.json
portfolio/accountgroups/account_groups_me_params.json
portfolio/accounts/accounts_me_params.json
portfolio/closedpositions/closed_position_list_params.json
portfolio/closedpositions/closed_position_subscription_params.json
portfolio/closedpositions/closed_positions_me_params.json
portfolio/exposure/remove_exposure_subscription_params.json
portfolio/exposure/remove_exposure_subscriptions_by_tag_params.json
portfolio/netpositions/net_positions_me_params.json
portfolio/orders/get_open_order_params.json
portfolio/orders/get_open_orders_me_params.json
portfolio/orders/remove_open_order_subscriptions_by_tag_params.json
portfolio/positions/position_list_subscription_params.json
portfolio/positions/positions_me_params.json
trading/prices/price_subscription_remove_by_tag_params.json
```

**これらは意図的な設計であり、エラーではありません。** これらのエンドポイントはパスパラメータのみを使用するか、パラメータが全く不要です。

## 検証

すべてのJSON Schemaファイルは以下のスクリプトで検証できます:

```bash
cd libs/saxo_openapi
uv run python scripts/validate_schemas.py
```

このスクリプトは以下をチェックします:
- JSON構文の正当性
- 空ファイルの検出
- 空文字列の検出（エラー）
- 空オブジェクトの検出（警告）

## 自動生成

これらのスキーマファイルは `scripts/convert_responses_to_json.py` によって自動生成されました。手動での編集は推奨されません。変更が必要な場合は、元の `saxo_openapi/endpoints/*/responses/*.py` ファイルを更新し、スクリプトを再実行してください。

## 関連ドキュメント

- API リファレンス: `../api/`
- 変換スクリプト: `../../scripts/convert_responses_to_json.py`
- 検証スクリプト: `../../scripts/validate_schemas.py`
