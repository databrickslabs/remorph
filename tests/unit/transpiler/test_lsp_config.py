from pathlib import Path
from typing import Any
from unittest.mock import patch

import copy
import pytest
import yaml

from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine
from tests.unit.conftest import path_to_resource


def test_valid_config():
    config = path_to_resource("lsp_transpiler", "config.yml")
    engine = LSPEngine.from_config_path(Path(config))
    assert engine.supported_dialects == ["snowflake"]


VALID_CONFIG: dict[str, Any] = yaml.safe_load(
    """remorph:
  version: 1
  dialects:
    - snowflake
    - oracle
  environment:
    - SOME_ENV: abc
  command_line:
    - python
    - lsp_server.py
custom:
  whatever: xyz
"""
)


def test_missing_version_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    del config["remorph"]["version"]
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Unsupported transpiler config version"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))


def test_invalid_version_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    config["remorph"]["version"] = 0
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Unsupported transpiler config version"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))


def test_missing_dialects_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    del config["remorph"]["dialects"]
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Missing dialects entry"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))


def test_empty_dialects_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    config["remorph"]["dialects"] = []
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Missing dialects entry"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))


def test_missing_cmd_line_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    del config["remorph"]["command_line"]
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Missing command_line entry"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))


def test_empty_cmd_line_raises_error():
    config = copy.deepcopy(VALID_CONFIG)
    config["remorph"]["command_line"] = []
    with (
        patch("pathlib.PosixPath.read_text", return_value=yaml.dump(config)),
        pytest.raises(ValueError, match="Missing command_line entry"),
    ):
        _ = LSPEngine.from_config_path(Path("stuff"))
