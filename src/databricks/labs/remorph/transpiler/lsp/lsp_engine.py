from __future__ import annotations

import abc
import asyncio
import logging
import os
from collections.abc import Callable, Sequence
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import attrs
import yaml

from lsprotocol import types as types_module
from lsprotocol.types import (
    InitializeParams,
    ClientCapabilities,
    InitializeResult,
    CLIENT_REGISTER_CAPABILITY,
    RegistrationParams,
    Registration,
    TextEdit,
    Diagnostic,
    DidOpenTextDocumentParams,
    TextDocumentItem,
    DidCloseTextDocumentParams,
    TextDocumentIdentifier,
    METHOD_TO_TYPES,
    LanguageKind,
    Range as LSPRange,
    Position as LSPPosition,
    DiagnosticSeverity,
)
from pygls.lsp.client import BaseLanguageClient
from pygls.exceptions import FeatureRequestError

from databricks.labs.blueprint.wheels import ProductInfo

from databricks.labs.remorph.config import TranspileConfig, TranspileResult
from databricks.labs.remorph.errors.exceptions import IllegalStateException
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from databricks.labs.remorph.transpiler.transpile_status import (
    TranspileError,
    ErrorKind,
    ErrorSeverity,
    CodeRange,
    CodePosition,
)

logger = logging.getLogger(__name__)


@dataclass
class _LSPRemorphConfigV1:
    name: str
    dialects: list[str]
    env_vars: dict[str, str]
    command_line: list[str]

    @classmethod
    def parse(cls, data: dict[str, Any]) -> _LSPRemorphConfigV1:
        version = data.get("version", 0)
        if version != 1:
            raise ValueError(f"Unsupported transpiler config version: {version}")
        name: str | None = data.get("name", None)
        if not name:
            raise ValueError("Missing 'name' entry")
        dialects = data.get("dialects", [])
        if len(dialects) == 0:
            raise ValueError("Missing 'dialects' entry")
        env_list = data.get("environment", [])
        env_vars: dict[str, str] = {}
        for env_var in env_list:
            env_vars = env_vars | env_var
        command_line = data.get("command_line", [])
        if len(command_line) == 0:
            raise ValueError("Missing 'command_line' entry")
        return _LSPRemorphConfigV1(name, dialects, env_vars, command_line)


@dataclass
class LSPConfig:
    path: Path
    remorph: _LSPRemorphConfigV1
    custom: dict[str, Any]

    @property
    def name(self):
        return self.remorph.name

    @classmethod
    def load(cls, path: Path) -> LSPConfig:
        yaml_text = path.read_text()
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid transpiler config, expecting a dict, got a {type(data).__name__}")
        remorph_data = data.get("remorph", None)
        if not isinstance(remorph_data, dict):
            raise ValueError(f"Invalid transpiler config, expecting a 'remorph' dict entry, got {remorph_data}")
        remorph = _LSPRemorphConfigV1.parse(remorph_data)
        custom = data.get("custom", {})
        return LSPConfig(path, remorph, custom)


def lsp_feature(
    name: str,
    options: Any | None = None,
):
    def wrapped(func: Callable):
        _LSP_FEATURES.append((name, options, func))
        return func

    return wrapped


_LSP_FEATURES: list[tuple[str, Any | None, Callable]] = []

# the below code also exists in lsp_server.py
# it will be factorized as part of https://github.com/databrickslabs/remorph/issues/1304
TRANSPILE_TO_DATABRICKS_METHOD = "document/transpileToDatabricks"


@attrs.define
class TranspileDocumentParams:
    uri: str = attrs.field()
    language_id: LanguageKind | str = attrs.field()


@attrs.define
class TranspileDocumentRequest:
    # 'id' is mandated by LSP
    # pylint: disable=invalid-name
    id: int | str = attrs.field()
    params: TranspileDocumentParams = attrs.field()
    method: Literal["document/transpileToDatabricks"] = "document/transpileToDatabricks"
    jsonrpc: str = attrs.field(default="2.0")


@attrs.define
class TranspileDocumentResult:
    uri: str = attrs.field()
    language_id: LanguageKind | str = attrs.field()
    changes: Sequence[TextEdit] = attrs.field()
    diagnostics: Sequence[Diagnostic] = attrs.field()


@attrs.define
class TranspileDocumentResponse:
    # 'id' is mandated by LSP
    # pylint: disable=invalid-name
    id: int | str = attrs.field()
    result: TranspileDocumentResult = attrs.field()
    jsonrpc: str = attrs.field(default="2.0")


def install_special_properties():
    is_special_property = getattr(types_module, "is_special_property")

    def customized(cls: type, property_name: str) -> bool:
        if cls is TranspileDocumentRequest and property_name in {"method", "jsonrpc"}:
            return True
        return is_special_property(cls, property_name)

    setattr(types_module, "is_special_property", customized)


install_special_properties()

METHOD_TO_TYPES[TRANSPILE_TO_DATABRICKS_METHOD] = (
    TranspileDocumentRequest,
    TranspileDocumentResponse,
    TranspileDocumentParams,
    None,
)


# subclass BaseLanguageClient so we can override stuff when required
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
            if registration.method == TRANSPILE_TO_DATABRICKS_METHOD:
                logger.debug(f"Registered capability: {registration.method}")
                self._transpile_to_databricks_capability = registration
                continue
            logger.debug(f"Unknown capability: {registration.method}")

    async def transpile_document_async(self, params: TranspileDocumentParams) -> TranspileDocumentResult:
        if self.stopped:
            raise RuntimeError("Client has been stopped.")
        await self._await_for_transpile_capability()
        return await self.protocol.send_request_async(TRANSPILE_TO_DATABRICKS_METHOD, params)

    async def _await_for_transpile_capability(self):
        for _ in range(1, 10):
            if self.transpile_to_databricks_capability:
                return
            await asyncio.sleep(0.1)
        if not self.transpile_to_databricks_capability:
            raise FeatureRequestError(f"LSP server did not register its {TRANSPILE_TO_DATABRICKS_METHOD} capability")

    # can't use @client.feature because it requires a global instance
    def _register_lsp_features(self):
        for name, options, func in _LSP_FEATURES:
            decorator = self.protocol.fm.feature(name, options)
            wrapper = self._wrapper_for_lsp_feature(func)
            decorator(wrapper)

    def _wrapper_for_lsp_feature(self, func):
        def wrapper(params):
            return func(self, params)

        return wrapper

    async def start_io(self, cmd: str, *args, **kwargs):
        await super().start_io(cmd, *args, **kwargs)
        # forward stderr
        task = asyncio.create_task(self.pipe_stderr())
        self._async_tasks.append(task)

    async def pipe_stderr(self):
        while not self._stop_event.is_set():
            data = await self._server.stderr.readline()
            message = data.decode("utf-8").strip()
            logger.error(message)


class ChangeManager(abc.ABC):

    @classmethod
    def apply(
        cls, source_code: str, changes: Sequence[TextEdit], diagnostics: Sequence[Diagnostic], file_path: Path
    ) -> TranspileResult:
        if not changes and not diagnostics:
            return TranspileResult(source_code, 1, [])
        transpile_errors = [DiagnosticConverter.apply(file_path, diagnostic) for diagnostic in diagnostics]
        try:
            lines = source_code.split("\n")
            for change in changes:
                lines = cls._apply(lines, change)
            transpiled_code = "\n".join(lines)
            return TranspileResult(transpiled_code, 1, transpile_errors)
        except IndexError as e:
            logger.error("Failed to apply changes", exc_info=e)
            error = TranspileError(
                code="INTERNAL_ERROR",
                kind=ErrorKind.INTERNAL,
                severity=ErrorSeverity.ERROR,
                path=file_path,
                message="Internal error, failed to apply changes",
            )
            transpile_errors.append(error)
            return TranspileResult(source_code, 1, transpile_errors)

    @classmethod
    def _apply(cls, lines: list[str], change: TextEdit) -> list[str]:
        new_lines = change.new_text.split("\n")
        if cls._is_full_document_change(lines, change):
            return new_lines
        # keep lines before
        result: list[str] = [] if change.range.start.line <= 0 else lines[0 : change.range.start.line]
        # special case where change covers full lines
        if change.range.start.character <= 0 and change.range.end.character >= len(lines[change.range.end.line]):
            pass
        # special case where change is within 1 line
        elif change.range.start.line == change.range.end.line:
            old_line = lines[change.range.start.line]
            if change.range.start.character > 0:
                new_lines[0] = old_line[0 : change.range.start.character] + new_lines[0]
            if change.range.end.character < len(old_line):
                new_lines[-1] += old_line[change.range.end.character :]
        else:
            if change.range.start.character > 0:
                old_line = lines[change.range.start.line]
                new_lines[0] = old_line[0 : change.range.start.character] + new_lines[0]
            if change.range.end.character < len(lines[change.range.end.line]):
                old_line = lines[change.range.end.line]
                new_lines[-1] += old_line[change.range.end.character :]
        result.extend(new_lines)
        # keep lines after
        if change.range.end.line < len(lines) - 1:
            result.extend(lines[change.range.end.line + 1 :])
        return result

    @classmethod
    def _is_full_document_change(cls, lines: list[str], change: TextEdit) -> bool:
        return (
            change.range.start.line <= 0
            and change.range.start.character <= 0
            and change.range.end.line >= len(lines) - 1
            and change.range.end.character >= len(lines[-1])
        )


class DiagnosticConverter(abc.ABC):

    _KIND_NAMES = {e.name for e in ErrorKind}

    @classmethod
    def apply(cls, file_path: Path, diagnostic: Diagnostic) -> TranspileError:
        code = str(diagnostic.code)
        kind = ErrorKind.INTERNAL
        parts = code.split("-")
        if len(parts) >= 2 and parts[0] in cls._KIND_NAMES:
            kind = ErrorKind[parts[0]]
            parts.pop(0)
            code = "-".join(parts)
        severity = cls._convert_severity(diagnostic.severity)
        lsp_range = cls._convert_range(diagnostic.range)
        return TranspileError(
            code=code, kind=kind, severity=severity, path=file_path, message=diagnostic.message, range=lsp_range
        )

    @classmethod
    def _convert_range(cls, lsp_range: LSPRange | None) -> CodeRange | None:
        if not lsp_range:
            return None
        return CodeRange(cls._convert_position(lsp_range.start), cls._convert_position(lsp_range.end))

    @classmethod
    def _convert_position(cls, lsp_position: LSPPosition) -> CodePosition:
        return CodePosition(lsp_position.line, lsp_position.character)

    @classmethod
    def _convert_severity(cls, severity: DiagnosticSeverity | None) -> ErrorSeverity:
        if severity == DiagnosticSeverity.Information:
            return ErrorSeverity.INFO
        if severity == DiagnosticSeverity.Warning:
            return ErrorSeverity.WARNING
        if severity == DiagnosticSeverity.Error:
            return ErrorSeverity.ERROR
        return ErrorSeverity.INFO


class LSPEngine(TranspileEngine):

    @classmethod
    def from_config_path(cls, config_path: Path) -> LSPEngine:
        config = LSPConfig.load(config_path)
        return LSPEngine(config_path.parent, config)

    def __init__(self, workdir: Path, config: LSPConfig):
        self._workdir = workdir
        self._config = config
        self._client = _LanguageClient()
        self._init_response: InitializeResult | None = None

    @property
    def supported_dialects(self) -> list[str]:
        return self._config.remorph.dialects

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
        # it is good practice to catch broad exceptions raised by launching a child process
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("LSP initialization failed", exc_info=e)
            os.chdir(cwd)

    async def _do_initialize(self, config: TranspileConfig) -> None:
        executable = self._config.remorph.command_line[0]
        env = deepcopy(os.environ)
        for name, value in self._config.remorph.env_vars.items():
            env[name] = value
        args = self._config.remorph.command_line[1:]
        logger.debug(f"Starting LSP engine: {executable} {args} (cwd={os.getcwd()})")
        await self._client.start_io(executable, env=env, *args)
        input_path = config.input_path
        root_path = input_path if input_path.is_dir() else input_path.parent
        params = InitializeParams(
            capabilities=self._client_capabilities(),
            root_uri=str(root_path.absolute().as_uri()),
            workspace_folders=None,  # for now, we only support a single workspace = root_uri
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
            "custom": self._config.custom,
        }

    async def shutdown(self):
        await self._client.shutdown_async(None)
        self._client.exit(None)
        await self._client.stop()

    @property
    def is_alive(self):
        return self._client.is_alive

    async def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path
    ) -> TranspileResult:
        self.open_document(file_path, source_code=source_code)
        response = await self.transpile_document(file_path)
        self.close_document(file_path)
        return ChangeManager.apply(source_code, response.changes, response.diagnostics, file_path)

    def open_document(self, file_path: Path, encoding="utf-8", source_code: str | None = None) -> None:
        if source_code is None:
            source_code = file_path.read_text(encoding)
        text_document = TextDocumentItem(
            uri=file_path.as_uri(), language_id=LanguageKind.Sql, version=1, text=source_code
        )
        params = DidOpenTextDocumentParams(text_document)
        self._client.text_document_did_open(params)

    def close_document(self, file_path: Path) -> None:
        text_document = TextDocumentIdentifier(uri=file_path.as_uri())
        params = DidCloseTextDocumentParams(text_document)
        self._client.text_document_did_close(params)

    async def transpile_document(self, file_path: Path) -> TranspileDocumentResult:
        params = TranspileDocumentParams(uri=file_path.as_uri(), language_id=LanguageKind.Sql)
        result = await self._client.transpile_document_async(params)
        return result
