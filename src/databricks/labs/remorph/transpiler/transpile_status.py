from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParserError:
    file_path: Path
    exception: str


@dataclass
class ValidationError:
    file_path: Path
    exception: str


@dataclass
class TranspileStatus:
    file_list: list[Path]
    no_of_queries: int
    parse_error_count: int
    validate_error_count: int
    error_log_list: list[ParserError | ValidationError] | None
