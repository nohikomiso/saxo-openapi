# 銘柄検索ワークフロー

この例では、`referencedata.instruments` モジュールを使用して、取引したい銘柄（Instrument）を検索する方法を示します。

## 前提条件

*   有効なアクセストークン

## コード例

```python
import json
from saxo_openapi import API
import saxo_openapi.endpoints.referencedata as rd

# 1. クライアントの初期化
token = "YOUR_ACCESS_TOKEN"
client = API(access_token=token)

# 2. 検索パラメータの設定
# 例: "Apple" を含む株式 (Stock) を検索
params = {
    "Keywords": "Apple",
    "AssetTypes": "Stock",
    "IncludeNonTradable": False,  # 取引可能なもののみ
    "Limit": 5                    # 上位5件のみ取得
}

# 3. リクエストの作成
# GET /openapi/ref/v1/instruments
r = rd.instruments.Instruments(params=params)

# 4. リクエストの実行
try:
    rv = client.request(r)
    print("検索結果:")
    # 結果の整形表示
    for item in rv['Data']:
        print(f"Name: {item['Description']}")
        print(f"Symbol: {item['Symbol']}")
        print(f"Uic: {item['Identifier']}")
        print(f"AssetType: {item['AssetType']}")
        print("-" * 30)
        
except Exception as e:
    print(f"検索失敗: {e}")
```

## 解説

1.  `saxo_openapi.endpoints.referencedata.instruments.Instruments` クラスを使用します。
2.  `params` 辞書で検索条件を指定します。
    *   `Keywords`: 検索したいキーワード（社名、シンボルなど）
    *   `AssetTypes`: 資産クラス（Stock, FxSpot, Bond など）。カンマ区切りで複数指定可能。
3.  レスポンスの `Data` リストに検索結果が含まれます。
4.  取引を行うには、ここで取得した `Identifier` (Uic) が必要になります。
