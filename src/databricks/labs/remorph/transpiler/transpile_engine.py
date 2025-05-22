from __future__ import annotations
import abc
from pathlib import Path

from databricks.labs.remorph.config import TranspileResult, TranspileConfig


class TranspileEngine(abc.ABC):

    @abc.abstractmethod
    async def initialize(self, config: TranspileConfig) -> None: ...

    @abc.abstractmethod
    async def shutdown(self) -> None: ...

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
