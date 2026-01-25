# Exposure

Exposure エンドポイントは、ポートフォリオのエクスポージャー（リスク量）情報を取得および管理するための機能を提供します。

## エンドポイント一覧

| クラス名 | メソッド | パス | 説明 |
|---------|----------|------|------|
| `NetInstrumentsExposureMe` | GET | /openapi/port/v1/exposure/instruments/me | ログインユーザーのネット・インストゥルメント・エクスポージャーを取得します。 |
| `NetInstrumentExposureSpecific` | GET | /openapi/port/v1/exposure/instruments/ | 指定されたクライアント/アカウントのネット・インストゥルメント・エクスポージャーを取得します。 |
| `CreateExposureSubscription` | POST | /openapi/port/v1/exposure/instruments/subscriptions | エクスポージャーのサブスクリプションを作成します。 |
| `RemoveExposureSubscriptionsByTag` | DELETE | /openapi/port/v1/exposure/instruments/subscriptions/{ContextId}/ | 指定されたコンテキストの全てのサブスクリプションを削除します。 |
| `RemoveExposureSubscription` | DELETE | /openapi/port/v1/exposure/instruments/subscriptions/{ContextId}/{ReferenceId} | 指定されたIDのサブスクリプションを削除します。 |
| `CurrencyExposureMe` | GET | /openapi/port/v1/exposure/currency/me | ログインユーザーの通貨エクスポージャーを取得します。 |
| `CurrencyExposureSpecific` | GET | /openapi/port/v1/exposure/currency/ | 指定されたクライアント/アカウントの通貨エクスポージャーを取得します。 |
| `FxSpotExposureMe` | GET | /openapi/port/v1/exposure/fxspot/me | ログインユーザーのFXスポットエクスポージャーを取得します。 |
| `FxSpotExposureSpecific` | GET | /openapi/port/v1/exposure/fxspot/ | 指定されたクライアント/アカウントのFXスポットエクスポージャーを取得します。 |

## 使用例

### 自分のネット・インストゥルメント・エクスポージャー取得 (NetInstrumentsExposureMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

r = exposure.NetInstrumentsExposureMe()
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/net_instruments_exposure_me_response.json)

### 特定のネット・インストゥルメント・エクスポージャー取得 (NetInstrumentExposureSpecific)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here",
    "AccountKey": "AccountKey_Here"
}

r = exposure.NetInstrumentExposureSpecific(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/net_instrument_exposure_specific_response.json)

### エクスポージャー・サブスクリプション作成 (CreateExposureSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

data = {
    "Arguments": {
        "AccountKey": "AccountKey_Here",
        "ClientKey": "ClientKey_Here"
    },
    "ContextId": "Context_Id",
    "ReferenceId": "Reference_Id"
}

r = exposure.CreateExposureSubscription(data=data)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/create_exposure_subscription_response.json)

### タグによるサブスクリプション削除 (RemoveExposureSubscriptionsByTag)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
params = {
    "Tag": "MyTag"
}

r = exposure.RemoveExposureSubscriptionsByTag(
    ContextId=context_id,
    params=params
)
client.request(r)

assert r.status_code == r.expected_status
```

### IDによるサブスクリプション削除 (RemoveExposureSubscription)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure

client = API(access_token="YOUR_ACCESS_TOKEN")

context_id = "Context_Id"
reference_id = "Reference_Id"

r = exposure.RemoveExposureSubscription(
    ContextId=context_id,
    ReferenceId=reference_id
)
client.request(r)

assert r.status_code == r.expected_status
```

### 自分の通貨エクスポージャー取得 (CurrencyExposureMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

r = exposure.CurrencyExposureMe()
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/currency_exposure_me_response.json)

### 特定の通貨エクスポージャー取得 (CurrencyExposureSpecific)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here"
}

r = exposure.CurrencyExposureSpecific(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/currency_exposure_specific_response.json)

### 自分のFXスポットエクスポージャー取得 (FxSpotExposureMe)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

r = exposure.FxSpotExposureMe()
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/fx_spot_exposure_me_response.json)

### 特定のFXスポットエクスポージャー取得 (FxSpotExposureSpecific)

```python
from saxo_openapi import API
from saxo_openapi.endpoints.portfolio import exposure
import json

client = API(access_token="YOUR_ACCESS_TOKEN")

params = {
    "ClientKey": "ClientKey_Here"
}

r = exposure.FxSpotExposureSpecific(params=params)
client.request(r)

print(json.dumps(r.response, indent=4))
```

[レスポンススキーマ](../../schemas/portfolio/exposure/fx_spot_exposure_specific_response.json)
