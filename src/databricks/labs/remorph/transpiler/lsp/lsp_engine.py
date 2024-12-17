from __future__ import annotations

import logging
import os
from collections.abc import Iterable, Callable, Sequence
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from lsprotocol.types import (
    InitializeParams,
    ClientCapabilities,
    InitializeResult,
    CLIENT_REGISTER_CAPABILITY,
    RegistrationParams,
    Registration, TextEdit, Diagnostic,
)
from pygls.lsp.client import BaseLanguageClient

from databricks.labs.blueprint.wheels import ProductInfo

from databricks.labs.remorph.config import TranspileConfig, TranspileResult
from databricks.labs.remorph.errors.exceptions import IllegalStateException
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine

logger = logging.getLogger(__name__)


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


def lsp_feature(
    name: str,
    options: Any | None = None,
):
    def wrapped(func: Callable):
        _LSP_FEATURES.append((name, options, func))
        return func

    return wrapped


_LSP_FEATURES: list[tuple[str, Any | None, Callable]] = []

TRANSPILE_TO_DATABRICKS_FEATURE = "document/transpileToDatabricks"

@dataclass
class TranspileParams:
    document_uri: str


@dataclass
class TranspileResponse:
    document_uri: str
    changes: Sequence[TextEdit]
    diagnostics: Sequence[Diagnostic]


# subclassing BaseLanguageClient so we can override stuff when required
class _LanguageClient(BaseLanguageClient):

    def __init__(self):
        version = ProductInfo.from_class(type(self)).version()
        super().__init__("Remorph", version)
        self._transpile_to_databricks_capability: Registration | None = None
        self._register_lsp_features()

    @property
    def is_alive(self):
        return self._server and self._server.returncode is None

    @property
    def transpile_to_databricks_capability(self):
        return self._transpile_to_databricks_capability

    @lsp_feature(CLIENT_REGISTER_CAPABILITY)
    def register_capabilities(self, params: RegistrationParams) -> None:
        for registration in params.registrations:
            if registration.method == TRANSPILE_TO_DATABRICKS_FEATURE:
                logger.debug(f"Registered capability: {registration.method}")
                self._transpile_to_databricks_capability = registration
                continue
            logger.debug(f"Unknown capability: {registration.method}")

    # can't use @client.feature because it requires a global instance
    def _register_lsp_features(self):
        for name, options, func in _LSP_FEATURES:
            decorator = self.protocol.fm.feature(name, options)
            wrapper = lambda params: func(self, params)
            decorator(wrapper)


class LSPEngine(TranspileEngine):

    @classmethod
    def from_config_path(cls, config_path: Path) -> LSPEngine:
        config, custom = cls._load_config(config_path)
        return LSPEngine(config_path.parent, config, custom)

    @classmethod
    def _load_config(cls, config_path: Path) -> tuple[_LSPRemorphConfigV1, dict[str, Any]]:
        yaml_text = config_path.read_text()
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid transpiler config, expecting a dict, got a {type(data).__name__}")
        remorph = data.get("remorph", None)
        if not isinstance(remorph, dict):
            raise ValueError(f"Invalid transpiler config, expecting a 'remorph' dict entry, got {remorph}")
        config = _LSPRemorphConfigV1.parse(remorph)
        return config, data.get("custom", {})

    def __init__(self, workdir: Path, config: _LSPRemorphConfigV1, custom: dict[str, Any]):
        self._workdir = workdir
        self._config = config
        self._custom = custom
        self._client = _LanguageClient()
        self._init_response: InitializeResult | None = None

    @property
    def supported_dialects(self) -> list[str]:
        return self._config.dialects

    @property
    def server_has_transpile_capability(self) -> bool:
        return self._client.transpile_to_databricks_capability is not None

    async def initialize(self, config: TranspileConfig) -> None:
        if self.is_alive:
            raise IllegalStateException("LSP engine is already initialized")
        cwd = os.getcwd()
        try:
            os.chdir(self._workdir)
            await self._do_initialize(config)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("LSP initialization failed", exc_info=e)
            os.chdir(cwd)

    async def _do_initialize(self, config: TranspileConfig) -> None:
        executable = self._config.command_line[0]
        env = deepcopy(os.environ)
        for name, value in self._config.env_vars.items():
            env[name] = value
        args = self._config.command_line[1:]
        await self._client.start_io(executable, env=env, *args)
        input_path = config.input_path
        root_path = input_path if input_path.is_dir() else input_path.parent
        params = InitializeParams(
            capabilities=self._client_capabilities(),
            root_path=str(root_path),
            initialization_options=self._initialization_options(config),
        )
        self._init_response = await self._client.initialize_async(params)

    def _client_capabilities(self):
        return ClientCapabilities()  # TODO do we need to refine this ?

    def _initialization_options(self, config: TranspileConfig):
        return {
            "remorph": {
                "source-dialect": config.source_dialect,
            },
            "custom": self._custom,
        }

    async def shutdown(self):
        await self._client.shutdown_async(None)
        self._client.exit(None)
        await self._client.stop()

    @property
    def is_alive(self):
        return self._client.is_alive

    def transpile(self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path) -> TranspileResult:
        raise NotImplementedError

    def analyse_table_lineage(
        self, source_dialect: str, source_code: str, file_path: Path
    ) -> Iterable[tuple[str, str]]:
        raise NotImplementedError
