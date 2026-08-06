"""Tests for packaged agent GUIDE."""

from pathlib import Path

import pytest
from saxo_api_client.agent import read_guide, write_guide
from saxo_api_client.agent.__main__ import main


def test_read_guide_contains_saxoclient():
    text = read_guide()
    assert "SaxoClient" in text
    assert "SaxoTrader" in text  # mentioned as removed
    assert "Layer 3" in text
    assert "PositionOpen" in text
    assert "PositionClose" in text
    assert "MarketCloseOrder" in text  # documented as removed
    assert "summarize_client_netting" in text
    assert "ForceOpenDefault" in text


def test_write_guide_to_file(tmp_path: Path):
    out = write_guide(tmp_path / "out.md")
    assert out.is_file()
    assert "SaxoClient" in out.read_text(encoding="utf-8")


def test_write_guide_to_directory(tmp_path: Path):
    out = write_guide(tmp_path)
    assert out.name == "GUIDE.md"
    assert out.is_file()


def test_cli_agent_guide_stdout(capsys):
    assert main(["agent-guide"]) == 0
    captured = capsys.readouterr()
    assert "SaxoClient" in captured.out


def test_cli_default_no_args(capsys):
    assert main([]) == 0
    assert "SaxoClient" in capsys.readouterr().out


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "1.3.0" in capsys.readouterr().out
