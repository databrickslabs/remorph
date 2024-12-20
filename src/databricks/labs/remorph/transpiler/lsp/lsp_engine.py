from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError


@dataclass
class _LSPRemorphConfigV1:
    dialects: list[str]
    env_vars: dict[str, str]
    command_line: list[str]

    @classmethod
    def parse(cls, data: dict[str, Any]) -> _LSPRemorphConfigV1:
        version = data.get("version", 0)
        if version != 1:
            raise ValueError(f"Unsupported transpiler config version: {version}")
        dialects = data.get("dialects", [])
        if len(dialects) == 0:
            raise ValueError("Missing dialects entry")
        env_list = data.get("environment", [])
        env_vars: dict[str, str] = {}
        for env_var in env_list:
            env_vars = env_vars | env_var
        command_line = data.get("command_line", [])
        if len(command_line) == 0:
            raise ValueError("Missing command_line entry")
        return _LSPRemorphConfigV1(dialects, env_vars, command_line)


class LSPEngine(TranspileEngine):

    @classmethod
    def from_config_path(cls, config_path: Path) -> LSPEngine:
        config, custom = cls._load_config(config_path)
        return LSPEngine(config, custom)

    @classmethod
    def _load_config(cls, config_path: Path) -> tuple[_LSPRemorphConfigV1, dict[str, Any]]:
        yaml_text = config_path.read_text()
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid transpiler config, expecting a dict, got a {type(data).__name__}")
        remorph = data.get("remorph", None)
        if not isinstance(remorph, dict):
            raise ValueError(f"Invalid transpiler config, expecting a 'remorh' dict entry, got {remorph}")
        config = _LSPRemorphConfigV1.parse(remorph)
        return config, data.get("custom", {})

    def __init__(self, config: _LSPRemorphConfigV1, custom: dict[str, Any]):
        self.config = config
        self.custom = custom

    @property
    def supported_dialects(self) -> list[str]:
        return self.config.dialects

    def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path, error_list: list[ParserError]
    ) -> TranspilationResult:
        raise NotImplementedError

    def check_for_unsupported_lca(self, source_dialect, source_code, file_path) -> ValidationError | None:
        raise NotImplementedError

    def analyse_table_lineage(
        self, source_dialect: str, source_code: str, file_path: Path
    ) -> Iterable[tuple[str, str]]:
        raise NotImplementedError
