import abc
from pathlib import Path

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError


class TranspileEngine(abc.ABC):

    @abc.abstractmethod
    def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path, error_list: list[ParserError]
    ) -> TranspilationResult: ...

    @abc.abstractmethod
    def check_for_unsupported_lca(self, source_dialect, source_code, file_path) -> ValidationError | None: ...
