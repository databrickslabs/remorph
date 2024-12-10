from __future__ import annotations
import abc
from pathlib import Path

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError


class TranspileEngine(abc.ABC):

    @classmethod
    def load_engine(cls, transpiler: Path) -> TranspileEngine:
        if str(transpiler) == "sqlglot":
            # pylint: disable=import-outside-toplevel, cyclic-import
            from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine

            return SqlglotEngine()
        if not transpiler.exists():
            raise ValueError(f"Error: Invalid value for '--transpiler': '{str(transpiler)}', file does not exist.")
        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine

        return LSPEngine(transpiler)

    @abc.abstractmethod
    def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path, error_list: list[ParserError]
    ) -> TranspilationResult: ...

    @abc.abstractmethod
    def check_for_unsupported_lca(self, source_dialect, source_code, file_path) -> ValidationError | None: ...

    @property
    @abc.abstractmethod
    def supported_dialects(self) -> list[str]: ...

    def check_source_dialect(self, source_dialect: str) -> str:
        if not source_dialect:
            if len(self.supported_dialects) == 1:
                return self.supported_dialects[0]
            else:
                raise ValueError(f"Missing value for '--source-dialect': '{source_dialect}'.")
        if source_dialect not in self.supported_dialects:
            raise ValueError(f"Invalid value for '--source-dialect': '{source_dialect}' is not one of {self.supported_dialects}.")
        return source_dialect
