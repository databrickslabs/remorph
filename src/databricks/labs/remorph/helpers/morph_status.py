from dataclasses import dataclass


@dataclass
class ParserError:
    file_name: str
    exception: str


@dataclass
class ValidationError:
    file_name: str
    exception: str


@dataclass
class MorphStatus:
    file_list: list[str]
    no_of_queries: int
    parse_error_count: int
    validate_error_count: int
    error_log_list: list[ParserError | ValidationError] | None
