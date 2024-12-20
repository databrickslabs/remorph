from __future__ import annotations
import abc
from collections.abc import Iterable
from pathlib import Path

from databricks.labs.remorph.config import TranspileResult


class TranspileEngine(abc.ABC):

    @classmethod
    def load_engine(cls, transpiler_config_path: Path) -> TranspileEngine:
        # TODO remove this once sqlglot transpiler is pluggable
        if str(transpiler_config_path) == "sqlglot":
            # pylint: disable=import-outside-toplevel, cyclic-import
            from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine

            return SqlglotEngine()
        if not transpiler_config_path.exists():
            raise ValueError(
                f"Error: Invalid value for '--transpiler-config-path': '{str(transpiler_config_path)}', file does not exist."
            )
        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine

        return LSPEngine.from_config_path(transpiler_config_path)

    @abc.abstractmethod
    def analyse_table_lineage(
        self, source_dialect: str, source_code: str, file_path: Path
    ) -> Iterable[tuple[str, str]]: ...

    @abc.abstractmethod
    async def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path
    ) -> TranspileResult: ...

    @property
    @abc.abstractmethod
    def supported_dialects(self) -> list[str]: ...

    def check_source_dialect(self, source_dialect: str) -> None:
        if source_dialect not in self.supported_dialects:
            raise ValueError(
                f"Invalid value for '--source-dialect': '{source_dialect}' is not one of {self.supported_dialects}."
            )
