from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar


@dataclass
class TransformRuleMapping:
    column_name: str
    transformation: str
    alias_name: str

    def get_column_expr_without_alias(self) -> str:
        if self.transformation:
            return f"{self.transformation}"
        return f"{self.column_name}"

    def get_column_expr_with_alias(self) -> str:
        return f"{self.get_column_expr_without_alias()} as {self.alias_name}"


@dataclass
class JdbcReaderOptions:
    number_partitions: int
    partition_column: str
    lower_bound: str
    upper_bound: str
    fetch_size: int = 100


@dataclass
class ColumnMapping:
    source_name: str
    target_name: str


@dataclass
class Transformation:
    column_name: str
    source: str
    target: str | None = None


@dataclass
class Thresholds:
    column_name: str
    lower_bound: str
    upper_bound: str
    type: str


@dataclass
class Filters:
    source: str = None
    target: str = None


@dataclass
class Table:
    source_name: str
    target_name: str
    join_columns: list[str] | None = None
    jdbc_reader_options: JdbcReaderOptions | None = None
    select_columns: list[str] | None = None
    drop_columns: list[str] | None = None
    column_mapping: list[ColumnMapping] | None = None
    transformations: list[Transformation] | None = None
    thresholds: list[Thresholds] | None = None
    filters: Filters | None = None

    Typ = TypeVar("Typ")

    def list_to_dict(self, cls: type[Typ], key: str) -> Typ:
        for _, value in self.__dict__.items():
            if isinstance(value, list):
                if all(isinstance(x, cls) for x in value):
                    return {getattr(v, key): v for v in value}
        return {}


@dataclass
class TableRecon:
    source_schema: str
    target_catalog: str
    target_schema: str
    tables: list[Table]
    source_catalog: str | None = None


@dataclass
class DatabaseConfig:
    source_schema: str
    target_catalog: str
    target_schema: str
    source_catalog: str | None = None


@dataclass
class Schema:
    column_name: str
    data_type: str
