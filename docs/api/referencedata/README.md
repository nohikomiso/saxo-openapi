# ReferenceData カテゴリ

参照データ取得のためのエンドポイント群

## 概要

ReferenceData カテゴリは、銘柄情報、通貨、取引所、標準日付など、取引に必要な参照データを提供します。これらのエンドポイントは、銘柄検索、通貨情報の取得、取引所情報の確認など、取引の準備段階で使用されます。

## 主なユースケース

- **銘柄検索**: 取引可能な銘柄の検索と詳細情報の取得
- **通貨情報**: サポートされている通貨の一覧と詳細
- **取引所情報**: 取引所の一覧と取引時間
- **国際化**: 言語、カルチャー、タイムゾーンの設定

## モジュール一覧

### [instruments](instruments.md) 👍 高優先度

取引可能な銘柄の情報を取得します。

- `Instruments`: 銘柄の一覧取得 (検索条件指定可能)
- `InstrumentsDetails`: 複数銘柄の詳細情報
- `InstrumentDetails`: 特定銘柄の詳細情報 (Uic と AssetType で指定)
- `ContractoptionSpaces`: オプション銘柄の詳細
- `FuturesSpaces`: 先物銘柄の詳細
- `TradingSchedule`: 銘柄の取引スケジュール

**主な用途**: 銘柄検索、銘柄情報の確認

---

### [currencies](currencies.md)

サポートされている通貨の情報を取得します。

- `Currencies`: 通貨一覧

**主な用途**: 通貨コードの確認、対応通貨の確認

---

### [exchanges](exchanges.md)

取引所の情報を取得します。

- `Exchanges`: 取引所一覧
- `ExchangeDetails`: 特定の取引所の詳細

**主な用途**: 取引所情報の確認、取引時間の確認

---

### [algostrategies](algostrategies.md)

アルゴリズム取引戦略の情報を取得します。

- `AlgoStrategies`: アルゴリズム戦略一覧

**主な用途**: アルゴリズム取引の設定

---

### [countries](countries.md)

国コードの情報を取得します。

- `Countries`: 国コード一覧

**主な用途**: 国設定、国コードの確認

---

### [cultures](cultures.md)

カルチャー (地域設定) の情報を取得します。

- `Cultures`: カルチャー一覧

**主な用途**: ロケール設定、言語・地域設定

---

### [currencypairs](currencypairs.md)

通貨ペアの情報を取得します。

- `CurrencyPairs`: 通貨ペア一覧

**主な用途**: FX 取引の通貨ペア確認

---

### [languages](languages.md)

サポートされている言語の情報を取得します。

- `Languages`: 言語一覧

**主な用途**: 言語設定の確認

---

### [standarddates](standarddates.md)

標準日付 (取引カレンダー) の情報を取得します。

- `StandardDates`: 標準日付一覧
- `StandardDateDetails`: 特定の標準日付の詳細

**主な用途**: 決済日の確認、取引カレンダーの確認

---

### [timezones](timezones.md)

タイムゾーンの情報を取得します。

- `TimeZones`: タイムゾーン一覧

**主な用途**: タイムゾーン設定の確認

---

## 関連するワークフロー例

- [銘柄検索](../../examples/search_instruments.md)

## よくある使い方

### 銘柄検索の例

```python
import saxo_openapi.endpoints.referencedata as ref
from saxo_openapi import API

client = API(access_token="YOUR_TOKEN")

# キーワードで銘柄を検索
params = {
    "Keywords": "Apple",
    "AssetTypes": "Stock",
    "$top": 10
}
r = ref.instruments.Instruments(params=params)
rv = client.request(r)

# 検索結果を表示
for instrument in rv.get('Data', []):
    print(f"{instrument['Symbol']} - {instrument['Description']}")
```

### 銘柄の詳細情報を取得

```python
# Uic と AssetType で特定の銘柄を取得 (例: Apple 株)
r = ref.instruments.InstrumentDetails(Uic=211, AssetType="Stock")
rv = client.request(r)

print(f"Symbol: {rv['Symbol']}")
print(f"Description: {rv['Description']}")
print(f"Exchange: {rv['Exchange']}")
```

## 次のステップ

- [Trading カテゴリ](../trading/README.md) - 銘柄の注文発注
- [Portfolio カテゴリ](../portfolio/README.md) - ポジション確認
- [API 全体索引](../README.md) - 全カテゴリ一覧
