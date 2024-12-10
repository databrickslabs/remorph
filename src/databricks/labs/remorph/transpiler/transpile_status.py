from dataclasses import dataclass
from pathlib import Path


@dataclass
class _BaseError:
    file_path: Path
    exception: str

    def __str__(self):
        return f"{type(self).__name__}(file_path='{self.file_path!s}', exception='{self.exception}')"


@dataclass
class ParserError(_BaseError):
    pass


@dataclass
class ValidationError(_BaseError):
    pass


@dataclass
class TranspileStatus:
    file_list: list[Path]
    no_of_queries: int
    parse_error_count: int
    validate_error_count: int
    error_log_list: list[ParserError | ValidationError] | None
