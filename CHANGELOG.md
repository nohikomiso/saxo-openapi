# Changelog

## Unreleased

### Added

- `SaxoClient.get_trading_availability`: TradingSchedule 優先、HTTP 404 時は
  Quote `MarketState` / InstrumentDetails `TradingStatus` にフォールバック
  （CfdOnIndex と CfdOnStock の取り違え等で schedule が無いケース向け）。

### Fixed

- `SaxoClient.get_positions_query` / `get_all_open_orders`: omit 時に `ClientKey` を
  `AccountsMe`（`client_key` プロパティ）から補完。PositionsQuery 400
  (`ClientKey field is required`) の踏み抜きを防止。
- `get_current_session_state`: 現在セッションを時間で判定。schedule 404 時は
  availability フォールバックを利用。

## 1.2.0 — 2026-07-20

### Breaking

- Removed `MarketCloseOrder`. Use `PositionClose.force_open_market` / `force_open_limit` /
  `force_open_stop` (or `SaxoClient.close_force_open_*`).

### Added

- `PositionOpen` — open-only factories (`market` / `limit` / `stop` / `stop_limit`) with
  mandatory `is_force_open`.
- `PositionClose` — close-only factories (`fifo_*` / `force_open_*` / `clear_force_open_market`).
- `SaxoClient`: `iter_open_positions`, `open_*`, `close_fifo_*`, `close_force_open_*`,
  `flatten_force_open`.
- Agent GUIDE / orders.md purpose decision table (open vs close, FIFO vs ForceOpen).
- MCP pitfalls section on ForceOpen fake flatten.
- CLI: `saxo-api-client --version` (reports package `__version__`).

### Changed

- Low-level `MarketOrder` / `LimitOrder` / `StopOrder` docstrings: prefer PositionOpen;
  forbid using them to close ForceOpen legs.
- Human docs: README (EN/JA), `docs/README.md`, quickstart, MIGRATION, samples README —
  open vs close / PositionOpen·PositionClose guidance.
- `docs/api/` reframed as Python binding index (MCP for OpenAPI params); examples fixed for
  `IsForceOpen` / `PositionOpen`.
- Sample `verify_cycle_trading_full.py`: open via `PositionOpen.market` (ForceOpen) to match
  `PositionClose.force_open_market` close path.

## 1.1.0 — 2026-07-19

### Added

- `SaxoClient.validate_order`, `stop_limit_order`, `stop_if_traded_order`.
- `docs/contrib/client.md` as the Layer 3 FX/Stock/CFD reference.
- **Agent-agnostic guide** shipped in the wheel: `saxo_api_client/agent/GUIDE.md`.
  - CLI: `saxo-api-client agent-guide` / `python -m saxo_api_client.agent`
  - API: `from saxo_api_client.agent import read_guide`
- README “For AI agents” section (EN/JA).
- Related Resources split: **AI → MCP (`mcp-server-saxo-openapi`)**; **humans → Markdown / official docs**.

### Changed

- Docs (EN/JA): Layer 3 documented as `SaxoClient` + `OptionTrader` (removed `SaxoTrader` docs/samples already gone since 1.0.0).
- README installation: prefer PyPI for both pip and uv; Git install is optional.
- Samples `verify_orders_live.py` / `verify_orders_precheck.py` migrated to `SaxoClient`.
- `SaxoClient.place_order` deduplicated and routed through `_execute_order` (AccountKey binding).

### Fixed

- Unit tests updated for required `IsForceOpen` on order builders and `OD.Direction` (not `BuySell`) in OptionTrader assertions.

## 1.0.0 — 2026-07-10

### Changed

- **Package rename:** PyPI `saxo-api-client`, import `saxo_api_client` (formerly `saxo-openapi` / `saxo_openapi` fork).
- **Breaking:** Not compatible with hootnot `saxo-api-client` 0.6.0 on PyPI. See README migration notes.
- `saxo_api_client.py` core module renamed to `client.py` (`from saxo_api_client import API` unchanged).

### Added

- `pyproject.toml` (hatchling) packaging for PyPI distribution.
