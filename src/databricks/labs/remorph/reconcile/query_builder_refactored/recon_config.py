from __future__ import annotations

from dataclasses import dataclass

from pyspark.sql import DataFrame


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
    source: str | None = None
    target: str | None = None


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

    @property
    def col_map(self):
        if self.column_mapping:
            return {c.source_name: c.target_name for c in self.column_mapping}
        return None

    def get_col_mapping(self, col: list[str] | set[str] | str, layer: str) -> set[str] | str:
        if layer == "source":
            return col
        if isinstance(col, list | set):
            columns = set()
            for c in col:
                columns.add(self.col_map.get(c, c))
            return columns
        else:
            return self.col_map.get(col, col)

    def get_select_columns(self, schema: list[Schema], layer: str) -> set[str]:
        if self.select_columns is None:
            return {sch.column_name for sch in schema}
        if self.col_map:
            return self.get_col_mapping(self.select_columns, layer)
        return set(self.select_columns)

    def get_threshold_columns(self, layer: str) -> set[str]:
        if self.thresholds is None:
            return set()
        return {self.get_col_mapping(thresh.column_name, layer) for thresh in self.thresholds}

    def get_join_columns(self, layer: str) -> set[str]:
        if self.join_columns is None:
            return set()
        return {self.get_col_mapping(col, layer) for col in self.join_columns}

    def get_drop_columns(self, layer: str) -> set[str]:
        if self.drop_columns is None:
            return set()
        return {self.get_col_mapping(col, layer) for col in self.drop_columns}

    def get_transformation_dict(self, layer: str) -> dict[str, str] | None:
        if self.transformations:
            if layer == "source":
                return {t.column_name: t.source for t in self.transformations}
            else:
                return {self.get_col_mapping(t.column_name, layer): t.target for t in self.transformations}
        return None

    def get_partition_column(self, layer: str) -> set[str]:
        if self.jdbc_reader_options and layer == "source":
            return {self.jdbc_reader_options.partition_column}
        return set()

    def get_filter(self, layer: str) -> str | None:
        if self.filters is None:
            return None
        if layer == "source":
            return self.filters.source
        return self.filters.target


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


@dataclass
class ReconcileOutput:
    missing_in_src: DataFrame
    missing_in_tgt: DataFrame
    mismatch: DataFrame | None = None
