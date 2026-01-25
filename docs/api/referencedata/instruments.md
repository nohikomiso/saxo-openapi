# ReferenceData Instruments

金融商品の情報を取得するためのエンドポイント群です。商品の検索、詳細情報の取得、オプション空間、先物空間、取引スケジュールなどの情報にアクセスできます。

## Endpoints

### Instruments

Saxo Trading プラットフォーム上のすべての金融商品とオプションのサマリー情報を取得します。ユーザーのアクセス権限により制限されます。

- **URL**: `openapi/ref/v1/instruments/`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータ（辞書）を渡します。

[Query Parameters Schema](../../schemas/referencedata/instruments/instruments_params.json)

#### Response

[Response Schema](../../schemas/referencedata/instruments/instruments_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {
    "AssetTypes": "Stock",
    "Keywords": "Apple"
}
r = rd.instruments.Instruments(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### InstrumentsDetails

複数の金融商品の詳細情報を取得します。

- **URL**: `openapi/ref/v1/instruments/details`
- **Method**: `GET`

#### Request

**Parameters**

クエリパラメータ（辞書）を渡します。

[Query Parameters Schema](../../schemas/referencedata/instruments/instruments_details_params.json)

#### Response

[Response Schema](../../schemas/referencedata/instruments/instruments_details_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
params = {
    "Uics": "21,22",
    "AssetTypes": "FxSpot"
}
r = rd.instruments.InstrumentsDetails(params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### InstrumentDetails

特定の金融商品の詳細情報を取得します。

- **URL**: `openapi/ref/v1/instruments/details/{Uic}/{AssetType}`
- **Method**: `GET`

#### Request

**Parameters**

- `Uic` (int, required): 商品のUIC
- `AssetType` (string, required): 資産タイプ
- `params` (dict, optional): クエリパラメータ

[Query Parameters Schema](../../schemas/referencedata/instruments/instrument_details_params.json)

#### Response

[Response Schema](../../schemas/referencedata/instruments/instrument_details_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
Uic = 22
AssetType = "FxSpot"
params = {"FieldGroups": ["OrderSetting"]}
r = rd.instruments.InstrumentDetails(Uic=Uic, AssetType=AssetType, params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### ContractoptionSpaces

コントラクトオプションのデータを取得します。

- **URL**: `openapi/ref/v1/instruments/contractoptionspaces/{OptionRootId}`
- **Method**: `GET`

#### Request

**Parameters**

- `OptionRootId` (string, required): オプションルートID
- `params` (dict, optional): クエリパラメータ

[Query Parameters Schema](../../schemas/referencedata/instruments/contractoption_spaces_params.json)

#### Response

[Response Schema](../../schemas/referencedata/instruments/contractoption_spaces_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
OptionRootId = "231"
params = {"FieldGroups": ["DisplayAndFormat"]}
r = rd.instruments.ContractoptionSpaces(OptionRootId=OptionRootId, params=params)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### FuturesSpaces

先物空間データを取得します。

- **URL**: `openapi/ref/v1/instruments/futuresspaces/{ContinuousFuturesUic}`
- **Method**: `GET`

#### Request

**Parameters**

- `ContinuousFuturesUic` (string, required): 連続先物UIC

#### Response

[Response Schema](../../schemas/referencedata/instruments/futures_spaces_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
ContinuousFuturesUic = "12345"
r = rd.instruments.FuturesSpaces(ContinuousFuturesUic=ContinuousFuturesUic)
client.request(r)
print(json.dumps(r.response, indent=2))
```

### TradingSchedule

取引スケジュールデータを取得します。1つのUICに対して複数の資産タイプが異なる時間で取引可能な場合があります。

- **URL**: `openapi/ref/v1/instruments/tradingschedule/{Uic}/{AssetType}`
- **Method**: `GET`

#### Request

**Parameters**

- `Uic` (string, required): 商品のUIC
- `AssetType` (string, required): 商品の資産タイプ

#### Response

[Response Schema](../../schemas/referencedata/instruments/trading_schedule_response.json)

#### Example

```python
import saxo_openapi
import saxo_openapi.endpoints.referencedata as rd
import json

client = saxo_openapi.API(access_token="YOUR_ACCESS_TOKEN")
Uic = "21"
AssetType = "FxSpot"
r = rd.instruments.TradingSchedule(Uic=Uic, AssetType=AssetType)
client.request(r)
print(json.dumps(r.response, indent=2))
```
