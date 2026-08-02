"""Tests for simulation vs live environment resolution."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from saxo_api_client.auth.models import APIEnvironment
from saxo_api_client.environment import (
    infer_environment_from_base_uri,
    infer_environment_from_token_filename,
    resolve_api_environment,
)


def test_infer_from_token_filename() -> None:
    assert infer_environment_from_token_filename("saxo_token_live_live.json") == "live"
    assert infer_environment_from_token_filename("saxo_token_demo_dev.json") == "simulation"
    assert infer_environment_from_token_filename("other.json") is None


def test_infer_from_base_uri() -> None:
    assert infer_environment_from_base_uri("https://gateway.saxobank.com/sim/openapi/") == "simulation"
    assert infer_environment_from_base_uri("https://gateway.saxobank.com/openapi/") == "live"
    assert infer_environment_from_base_uri(None) is None


def test_resolve_from_auth_client_live() -> None:
    auth = MagicMock()
    auth._app_config.env = APIEnvironment.LIVE
    assert resolve_api_environment(auth_client=auth) == "live"


def test_resolve_from_auth_client_sim() -> None:
    auth = MagicMock()
    auth._app_config.env = APIEnvironment.SIM
    assert resolve_api_environment(auth_client=auth) == "simulation"


def test_resolve_explicit_overrides_auth_client() -> None:
    auth = MagicMock()
    auth._app_config.env = APIEnvironment.LIVE
    assert resolve_api_environment(explicit="simulation", auth_client=auth) == "simulation"


def test_resolve_defaults_simulation() -> None:
    assert resolve_api_environment() == "simulation"


def test_resolve_token_file_live_name(tmp_path: Path) -> None:
    token = tmp_path / "saxo_token_live_live.json"
    token.write_text('{"access_token": "x"}', encoding="utf-8")
    assert resolve_api_environment(token_file=token, token_data={"access_token": "x"}) == "live"


def test_resolve_unknown_explicit_raises() -> None:
    with pytest.raises(KeyError, match="Unknown environment"):
        resolve_api_environment(explicit="staging")
