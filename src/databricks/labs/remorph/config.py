from dataclasses import dataclass


@dataclass
class MorphConfig:
    source: str
    input_sql: str
    output_folder: str | None
    skip_validation: bool = False
    catalog_name: str = "transpiler_test"
    schema_name: str = "convertor_test"
