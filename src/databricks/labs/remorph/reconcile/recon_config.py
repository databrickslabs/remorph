from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TypeVar

from sqlglot import expressions as exp

from databricks.labs.remorph.reconcile.constants import ThresholdMode

logger = logging.getLogger(__name__)


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

    def get_mode(self):
        return (
            ThresholdMode.PERCENTILE.value
            if "%" in self.lower_bound or "%" in self.upper_bound
            else ThresholdMode.ABSOLUTE.value
        )

    def get_type(self):
        if any(self.type in numeric_type.value.lower() for numeric_type in exp.DataType.NUMERIC_TYPES):
            if self.get_mode() == ThresholdMode.ABSOLUTE.value:
                return ThresholdMode.NUMBER_ABSOLUTE.value
            return ThresholdMode.NUMBER_PERCENTILE.value

        if any(self.type in numeric_type.value.lower() for numeric_type in exp.DataType.TEMPORAL_TYPES):
            return ThresholdMode.DATETIME.value

        error_message = f"Threshold type {self.type} not supported in column {self.column_name}"
        logger.error(error_message)
        raise ValueError(error_message)


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

    @property
    def get_threshold_columns(self) -> set[str]:
        return {thresh.column_name for thresh in self.thresholds or []}

    @property
    def get_join_columns(self) -> set[str]:
        if self.join_columns is None:
            return set()
        return set(self.join_columns)

    @property
    def get_drop_columns(self) -> set[str]:
        if self.drop_columns is None:
            return set()
        return set(self.drop_columns)

    def get_partition_column(self, layer) -> set[str]:
        if self.jdbc_reader_options and layer == "source":
            return {self.jdbc_reader_options.partition_column}
        return set()

    def get_filter(self, layer) -> str:
        if self.filters is None:
            return " 1 = 1 "
        if layer == "source":
            return self.filters.source
        return self.filters.target

    def get_threshold_info(self, column: str):
        return next((threshold for threshold in self.thresholds if threshold.column_name == column), None)


@dataclass
class Schema:
    column_name: str
    data_type: str
