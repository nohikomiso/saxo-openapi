"""Resolve REST API environment (simulation vs live) for saxo_api_client."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

TRADING_ENVIRONMENTS = {
    "simulation": {
        "stream": "https://sim-streaming.saxobank.com",
        "api": "https://gateway.saxobank.com",
        "prefix": "sim",
    },
    "live": {
        "stream": "https://live-streaming.saxobank.com",
        "api": "https://gateway.saxobank.com",
    },
}

ApiEnvironmentName = Literal["simulation", "live"]


def infer_environment_from_base_uri(base_uri: str | None) -> ApiEnvironmentName | None:
    """Infer environment from OAuth token ``base_uri`` when present."""
    if not base_uri:
        return None
    lower = str(base_uri).lower()
    if "/sim/" in lower or "simulation" in lower:
        return "simulation"
    return "live"


def infer_environment_from_token_filename(token_file: str | Path) -> ApiEnvironmentName | None:
    """Infer environment from common token file naming (``saxo_token_live_*`` / ``demo_*``)."""
    name = Path(token_file).name
    if name.startswith("saxo_token_live_"):
        return "live"
    if name.startswith("saxo_token_demo_"):
        return "simulation"
    return None


def infer_environment_from_auth_client(auth_client: Any) -> ApiEnvironmentName | None:
    """Infer environment from ``SaxoAuthClient`` app config (LIVE vs SIM)."""
    try:
        from saxo_api_client.auth.models import APIEnvironment

        app_config = auth_client._app_config
        env = app_config.env
        if env == APIEnvironment.LIVE:
            return "live"
        if env == APIEnvironment.SIM:
            return "simulation"
    except Exception:
        return None
    return None


def load_token_json(token_file: str | Path) -> dict[str, Any]:
    """Load token JSON written by OAuth or 24h dev flow."""
    path = Path(token_file)
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_api_environment(
    *,
    explicit: str | None = None,
    auth_client: Any | None = None,
    base_uri: str | None = None,
    token_file: str | Path | None = None,
    token_data: dict[str, Any] | None = None,
) -> ApiEnvironmentName:
    """Resolve REST gateway environment with safe fallbacks.

    Priority:
    1. ``explicit`` argument
    2. ``auth_client._app_config.env``
    3. ``token_file`` name (``saxo_token_live_*`` / ``saxo_token_demo_*``)
    4. ``base_uri`` or ``token_data['base_uri']``
    5. default ``simulation`` (documented — Live tokens need explicit or hints above)
    """
    if explicit is not None:
        if explicit not in TRADING_ENVIRONMENTS:
            raise KeyError(f"Unknown environment: {explicit!r}. Use 'simulation' or 'live'.")
        return explicit  # type: ignore[return-value]

    if auth_client is not None:
        from_auth = infer_environment_from_auth_client(auth_client)
        if from_auth is not None:
            return from_auth

    if token_file is not None:
        from_name = infer_environment_from_token_filename(token_file)
        if from_name is not None:
            return from_name
        if token_data is None:
            path = Path(token_file)
            if path.is_file():
                token_data = load_token_json(path)

    if token_data is not None and base_uri is None:
        raw = token_data.get("base_uri") or token_data.get("BaseUri")
        base_uri = str(raw) if raw else None

    from_uri = infer_environment_from_base_uri(base_uri)
    if from_uri is not None:
        return from_uri

    return "simulation"
