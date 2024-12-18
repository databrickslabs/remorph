import abc
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TranspileError(abc.ABC):
    file_path: Path
    error_msg: str

    def __str__(self):
        return f"{type(self).__name__}(file_path='{self.file_path!s}', error_msg='{self.error_msg}')"


@dataclass
class ParserError(TranspileError):
    pass


@dataclass
class ValidationError(TranspileError):
    pass


@dataclass
class TranspileStatus:
    file_list: list[Path]
    no_of_transpiled_queries: int
    parse_error_count: int
    validate_error_count: int
    error_list: list[TranspileError]
