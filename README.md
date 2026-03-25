# Saxo-OpenAPI (AI-Ready)

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![AI-First](https://img.shields.io/badge/AI--First-Optimized-success.svg)
![Type Safety](https://img.shields.io/badge/Type%20Safety-Strictly%20Typed-blue.svg)
![Docs](https://img.shields.io/badge/Docs-AI--Ready-orange.svg)

Saxo Bank OpenAPI を Python から効率的かつ安全に利用するための、**AI アシスタントへの最適化 (AI-First)** を施した現代的なクライアントライブラリです。

このライブラリは、オリジナルの [hootnot/saxo_openapi](https://github.com/hootnot/saxo_openapi) をベースに、AI 時代の開発フローに合わせてアーキテクチャから再設計されたフォーク・バージョンです。**今日の発展は、オリジナルの作者である hootnot 氏による多大なる初期の努力と実装があったからこそ実現しました。**

---

## 💎 特徴：AI-First Documentation

本ライブラリの最大の特徴は、AI アシスタント（Claude, GPT-4, Gemini 等）が最小限のトークン消費で正確な情報を取得し、ユーザーをサポートできるように設計されている点です。

1. **ドキュメントの完全分離**: Python コードから詳細な docstring を外部の Markdown ファイル（`docs/api/`）へ移管。AI は必要な時に必要なドキュメントだけを参照するため、コンテキストを節約できます。
2. **AI ナビゲーション (`.ai/index.json`)**: 全エンドポイント、カテゴリ、ユースケースを構造化された JSON メタデータで管理。AI は目的のエンドポイントを瞬時に検索可能です。
3. **豊富な実行例とスキーマ**: 275個以上の JSON Schema (`docs/schemas/`) と、すぐに試せるワークフロー例 (`docs/examples/`) が用意されています。
4. **厳格な型定義 (Python 3.13+)**: `mypy` 等での静的解析を前提とした設計により、開発時のバグを未然に防ぎます。
5. **動的レート制限処理**: API からの 429 エラーを検知し、リセット時間を動的に解析して自動待機・リトライを行います。
6. **強力な認証サポート**: OAuth 2.0 認証とセッション管理は、[Saxo-APY (認証クライアント)](https://github.com/nohikomiso/saxo-apy) との連携を強く推奨します。

---

## 📚 ドキュメントポータル

詳細な情報は `docs/` ディレクトリ内の各ガイドを参照してください。

- **[総合インデックス (docs/README.md)](docs/README.md)** - ドキュメント全体の入り口
- **[クイックスタート (docs/quickstart.md)](docs/quickstart.md)** - 5分で最初のリクエストを実行
- **[認証ガイド (docs/authentication.md)](docs/authentication.md)** - 接続設定とトークン管理
- **[AI-First 移行ガイド (docs/MIGRATION.md)](docs/MIGRATION.md)** - 旧アーキテクチャからの変更点

---

## 🚀 クイックスタート

### インストール

```bash
uv add libs/saxo_openapi/
# または
pip install -e libs/saxo_openapi/
```

### 最初のリクエスト

```python
import os
from saxo_openapi import API
import saxo_openapi.endpoints.portfolio as pf

# クライアントの初期化（環境変数からトークンを取得）
client = API(access_token=os.getenv("SAXO_ACCESS_TOKEN"))

# 残高確認リクエスト（詳細は docs/api/portfolio/balances.md を参照）
r = pf.balances.AccountBalancesMe()
rv = client.request(r)

print(rv)
```

---

## 🛠 推奨されるシステム構成

本ライブラリを最大限に活用し、24 時間 365 日安定したアルゴリズム取引を実現するための「推奨構成（マルチサービス・アーキテクチャ）」を紹介します。

### 1. 認証と操作の分離 (Separation of Concerns)
認証管理と実際の取引・データ取得ロジックを別々のプロセスとして運用する構成です。

- **認証サービス (Auth Service)**: [Saxo-APY](https://github.com/nohikomiso/saxo-apy) を使用。OAuth 認証を行い、取得したトークンを常に最新の状態に保ちながらファイル（例: `saxo_token.json`）に保存し続けます。
- **取引サービス (Trading Services)**: 本ライブラリ（Saxo-OpenAPI）を使用。保存されたトークンファイルを読み込むだけで、認証手順を気にすることなく「残高取得」「価格監視」「注文執行」といった本来のロジックに集中できます。

### 2. メリット
- **堅牢性**: 認証エラーが発生しても、取引ロジック自体を再起動することなく、認証サービス側で復旧を試みることができます。
- **拡張性**: 1 つの共通トークンファイルを参照することで、「監視サービス」「執行サービス」「通知サービス」など、複数の独立したプロセスを容易に追加・同時稼働させることが可能です。

---

## ⚠️ 注意事項：ストリーミング機能について

本ライブラリ（Saxo-OpenAPI）に含まれるストリーミング関連の機能は、現時点では「開発途上（不十分）」な状態です。

- **サポート範囲**: 主に **「ストリーミング接続の確立」** および **「サブスクリプション（購読）の登録」** 程度しか正常動作が確認されていません。
- **不足している機能**: 受信メッセージの効率的なデコード、動的な再接続ロジック、複雑な並列処理、およびパフォーマンスの最適化などは実装されていません。
- **推奨事項**: 本格的なリアルタイムトレードや大規模なデータ取得を行う場合は、本ライブラリの内蔵機能に頼らず、**用途に合わせた独自のストリーミング受信実装を構築することを強く推奨します。**

---

## 📂 ディレクトリ構成

- `saxo_openapi/`: ライブラリの本体コード。ロジックに集中した最小限の docstring。
- `docs/api/`: **[メイン]** 全エンドポイントの日本語ドキュメント。
- `docs/schemas/`: リクエスト/レスポンスの JSON Schema 群（約 270 ファイル）。
- `docs/examples/`: 実践的なワークフロー例（残高確認、注文、ストリーミング等）。
- `saxo_openapi/contrib/`: 注文作成を簡素化する高機能ヘルパークラス (`SaxoTrader` 等)。
- `samples/`: **[NEW]** 実環境での動作を検証するためのサンプルスクリプト群（FX, オプション, 注文ライフサイクル等）。
- `tests/`: ライブラリ自体の単体テスト・結合テスト。
- `.ai/`: AI アシスタント用の構造化インデックスとメトリクス。

---

## 🧪 検証とテスト

`samples/` ディレクトリには、実際の取引シナリオをシミュレートする検証スクリプトが豊富に用意されています：
- `verify_lifecycle_trading.py`: 注文の発注から約定までのライフサイクル動作確認
- `verify_refdata_fx.py`: 通貨ペアの参照データ取得
- `verify_portfolio_fx.py`: ポートフォリオの残高・ポジション確認

これらのスクリプトは、ライブラリの正しい動作を実環境で確認するための最良のリファレンスとなります。

また、単体テストは以下のコマンドで実行可能です：
```bash
pytest tests/
```

---

## 🔗 関連リソース

- **[SaxoBank OpenAPI Docs (Markdown版)](https://github.com/nohikomiso/SaxoBank-OpenAPI-Docs)**: Saxo 公式ドキュメントの Markdown 公開版。

---

## 🙏 謝辞 (Acknowledgments)

本プロジェクトの核心的なコードベース、および Saxo OpenAPI を Python で叩くための基盤は、元々 **[hootnot (GitHub)](https://github.com/hootnot)** 氏によって情熱を持って開発されました。

氏が長年をかけて積み上げた実装、そして Saxo OpenAPI への深い理解に基づく初期の設計があったからこそ、私はこの強力な「AI-First」な新世代ライブラリへと進化させることができました。**たとえ現在のメンテナンス状況がどうあれ、氏の先駆的な貢献と多大な努力に対し、心から最大の敬意と感謝を表します。**

## ⚖️ ライセンス

MIT License (オリジナルのライセンスを継承)。詳細は `LICENSE` を参照してください。
