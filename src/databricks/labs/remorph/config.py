from dataclasses import dataclass


@dataclass
class MorphConfig:
    source: str
    input_sql: str
    output_folder: str
    skip_validation: str = "false"
    validation_mode: str = "LOCAL_REMOTE"
    catalog_nm: str = "transpiler_test"
    schema_nm: str = "convertor_test"


@dataclass
class MorphStatus:
    file_list: list[str]
    no_of_queries: int
    parse_error_count: int
    validate_error_count: int
    error_log_list: list[str]
