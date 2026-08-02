# saxo-api-client — Agent Guide (canonical)

**Audience:** any AI coding agent (Cursor, Claude, Codex, Windsurf, etc.).  
**Source of truth:** this file, shipped inside the installed package. Do not invent a parallel “SaxoTrader” layer.

```bash
# After: pip install saxo-api-client  OR  uv add saxo-api-client
saxo-api-client agent-guide
# or
python -m saxo_api_client.agent
```

Human docs: package README (English canonical) / README.ja.md (Japanese translation).  
Repo docs (clone only): `docs/contrib/client.md`, `docs/MIGRATION.md`.

---

## Entry points (use these)

| Goal | Use |
|------|-----|
| FX / Stock / CFD trading | `from saxo_api_client.contrib.client import SaxoClient` |
| Stock options / multileg | `from saxo_api_client.contrib.option_trader import OptionTrader` |
| Auth / OAuth | `from saxo_api_client.auth import SaxoAuthClient` |
| Raw REST | `from saxo_api_client import API` + `saxo_api_client.endpoints.*` |

**Removed:** `saxo_api_client.contrib.trader.SaxoTrader` — no shim. Always use `SaxoClient`.  
**Removed:** `MarketCloseOrder` — use `PositionClose.force_open_*`.

---

## Architecture (do not flatten)

1. **Layer 3 — Facades (preferred):** `SaxoClient`, `OptionTrader`  
   Prefer intent methods: `open_*` / `close_fifo_*` / `close_force_open_*` / `flatten_force_open`.
2. **Layer 2 — Intent builders:** `PositionOpen`, `PositionClose`  
   Low-level: `MarketOrder`, `LimitOrder`, `StopOrder` (open-only; never FO close).
3. **Layer 1 — FlexModels:** Pydantic OpenAPI models (usually automatic).
4. **Layer 0 — Transport:** `API`, `endpoints.*`, `SaxoAuthClient`.

Rule: start at Layer 3; drop to Layer 2/0 only for uncovered edge cases.

---

## Open vs close (anti-hallucination)

Before coding, answer these four questions:

1. Open or close? → `PositionOpen` / `PositionClose` (or `client.open_*` / `client.close_*`)
2. If close: FIFO or ForceOpen? → `fifo_*` / `force_open_*`
3. Market / limit / stop?
4. If ForceOpen close: get `position_id` from `client.iter_open_positions` (top-level PositionsQuery id). No id → do not close.

| Intent | API |
|--------|-----|
| New limit/stop | `PositionOpen.limit` / `.stop` (`is_force_open` required) |
| FIFO close limit/stop | `PositionClose.fifo_limit` / `.fifo_stop` |
| FO close limit/stop | `PositionClose.force_open_limit` / `.force_open_stop` (`position_id` required) |

**Forbidden**

- Closing ForceOpen with standalone `StopOrder` / `LimitOrder` / `MarketOrder` (opens opposite leg = fake close)
- Using `PositionClose` to open a new position
- A single ambiguous `close_position()` that guesses FIFO vs FO

```python
# BAD — FO long “close” via standalone stop (actually opens short)
StopOrder(Uic=42, Amount=-10000, OrderPrice=entry, IsForceOpen=False, ...)

# GOOD
from saxo_api_client.contrib.orders import PositionClose
PositionClose.force_open_stop(
    position_id=pid, uic=42, amount=10000, asset_type="FxSpot",
    buy_sell="Sell", order_price=entry,
)
```

---

## SaxoClient — minimal patterns

```python
from saxo_api_client.contrib.client import SaxoClient

# Simulation default (access_token only)
client = SaxoClient(access_token="...")

# Live: environment="live" | from_token_file(...) | auth_client=...
client = SaxoClient.from_token_file("saxo_token_live_live.json")

# Preferred: intent-named open/close
client.open_market(
    asset_type="FxSpot", uic=42, amount=10000, buy_sell="Buy", is_force_open=True,
)
rows = client.iter_open_positions(uic=42)
pid = rows[0]["position_id"]
client.close_force_open_market(
    position_id=pid, asset_type="FxSpot", uic=42, amount=10000, buy_sell="Sell",
)
client.flatten_force_open(asset_type="FxSpot", uic=42)

# Legacy one-liners (low-level; amount sign = side). Prefer open_*/close_* for FO.
client.market_order(asset_type="FxSpot", uic=21, amount=10000, IsForceOpen=False)
client.validate_order(order_builder_instance)
client.cancel_order(order_id)
```

Keyword style: `asset_type` first; resolve with `symbol=` and/or `uic=`.

`IsForceOpen`: stripped automatically for Stock; allowed for FX/CFD (hedging).

---

## Account defaults vs explicit orders

Before placing orders (startup / preflight), log:

```python
summary = client.summarize_client_netting()
# notes[] may warn on EndOfDay zombies or ForceOpenDefaultValue=True
```

- **GUI / `ForceOpenDefaultValue`**: omit-time defaults only. Explicit `is_force_open=` / FO `position_id` / Option `ToOpenClose` win.
- **`EndOfDay`**: closed legs may still appear in positions until EOD — do not re-close (zombie).
- **Do not** auto-switch `close_fifo_*` vs `close_force_open_*` from account mode. Choose by intent + whether the leg is ForceOpen (and AssetType for options).

---

## Pitfalls (read before placing orders)

- Prefer **simulation** tokens and `validate_order` before live placement.
- **`access_token` only → simulation gateway.** Live tokens need `environment="live"`, `SaxoClient.from_token_file`, or `auth_client` (infers from `app_config`). 401 on `/sim/openapi/` usually means environment mismatch.
- Rate limits: SessionOrders is strict; space order calls (~1s).
- ForceOpen close requires **PositionId + nested Orders** — never standalone opposite stop/limit.
- Do not invent undocumented fields; prefer Layer 3 methods.
- Streaming helpers are incomplete — do not rely on them for production market data.
- Wheel does **not** ship full `docs/` or `.ai/`; this GUIDE + README are the installed agent sources. Clone the repo for full docs.

---

## How to deepen (if repo or docs available)

1. **MCP (preferred for agents):** PyPI `mcp-server-saxo-openapi` — endpoint search, nested specs, `saxo://docs/pitfalls.md`. Not a trading client.
2. README 3-tier section and this GUIDE  
3. `docs/contrib/client.md` / `orders.md` / `option_trader.md` (clone)  
4. Human browsing: [SaxoBank OpenAPI Docs Markdown](https://github.com/nohikomiso/SaxoBank-OpenAPI-Docs) or [official reference](https://www.developer.saxo/openapi/referencedocs)

Do **not** treat removed `SaxoTrader` / `MarketCloseOrder` docs/samples as current API.
