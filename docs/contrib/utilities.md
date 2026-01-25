# Contrib Utilities

`saxo_openapi.contrib` パッケージには、API 操作を簡素化するためのユーティリティモジュールが含まれています。

## セッションユーティリティ

`saxo_openapi.contrib.session` モジュールは、アカウント情報を簡単に取得するためのヘルパー関数を提供します。

### インポート

```python
from saxo_openapi.contrib import session
```

### account_info

ログイン中のユーザーの主要なアカウント情報を取得します（最初のアカウント）。

```python
ai = session.account_info(client)
print(ai.ClientKey)
print(ai.AccountKey)
```

**引数:**
*   `client`: API クライアントインスタンス。

**戻り値:**
*   `namedtuple`: `ClientId`, `ClientKey`, `AccountId`, `AccountKey` を含む名前付きタプル。

### account_info2

ログイン中のユーザーの2番目のアカウント情報を取得します（存在する場合）。
主にテストや特定のアカウント構成を持つユーザー向けです。

```python
ai = session.account_info2(client)
```

## 一般ユーティリティ

`saxo_openapi.contrib.util` モジュールは、一般的なタスクのためのユーティリティ関数を提供します。

### インポート

```python
from saxo_openapi.contrib.util import InstrumentToUic
```

### InstrumentToUic

辞書内の `Instrument`（銘柄名やシンボル）を検索し、対応する `Uic`（Universal Instrument Code）に置き換えます。
API リクエストを作成する際、シンボル名から直接 Uic を解決してリクエストボディを構築するのに便利です。

```python
spec = {
    'Instrument': 'EURUSD',
    'Amount': 10000
}

# Instrument='EURUSD' を検索し、Uic=21 に置き換え
updated_spec = InstrumentToUic(
    client=client,
    AccountKey=AccountKey,
    spec=spec,
    assettype=OD.AssetType.FxSpot
)

print(updated_spec)
# {'Amount': 10000, 'Uic': 21}
```

**引数:**
*   `client`: API クライアントインスタンス。
*   `AccountKey`: アカウントキー。
*   `spec` (dict): 処理対象の辞書。`Instrument` キーが含まれている場合、API を検索して `Uic` に置換します。
*   `assettype` (str, optional): 検索に使用する資産タイプ。デフォルトは `FxSpot`。

**例外:**
*   `ValueError`: 複数の銘柄が見つかった場合、または検索に失敗した場合。
