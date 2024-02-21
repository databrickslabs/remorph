from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from databricks.sdk.service._internal import _from_dict, _repeated_dict

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.utils import filter_list


# [TODO]: Move _internal to blueprint


@dataclass
class TransformRuleMapping:
    column_name: str
    transformation: Optional[str]
    alias_name: Optional[str]

    def get_column_expression_without_alias(self) -> str:
        if self.transformation:
            return f"{self.transformation}"
        else:
            return f"{self.column_name}"

    def get_column_expression_with_alias(self) -> str:
        if self.alias_name:
            return f"{self.get_column_expression_without_alias} as {self.alias_name}"
        else:
            return f"{self.get_column_expression_without_alias} as {self.column_name}"


@dataclass
class JdbcReaderOptions:
    number_partitions: int
    partition_column: str
    lower_bound: str
    upper_bound: str
    fetch_size: int = 100

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> JdbcReaderOptions:
        """Deserializes the JdbcReaderOptions from a dictionary."""
        return cls(
            number_partitions=d.get("number_partitions"),
            partition_column=d.get("partition_column"),
            lower_bound=d.get("lower_bound"),
            upper_bound=d.get("upper_bound"),
            fetch_size=d.get("fetch_size", 100),
        )


@dataclass
class JoinColumns:
    source_name: str
    target_name: Optional[str]

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> JoinColumns:
        """Deserializes the JoinColumns from a dictionary."""
        return cls(source_name=d.get("source_name"), target_name=d.get("target_name"))


@dataclass
class ColumnMapping:
    source_name: str
    target_name: str

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> ColumnMapping:
        """Deserializes the ColumnMapping from a dictionary."""
        return cls(source_name=d.get("source_name"), target_name=d.get("target_name"))


@dataclass
class Transformation:
    column_name: str
    source: str
    target: str

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> Transformation:
        """Deserializes the Transformations from a dictionary."""
        return cls(column_name=d.get("column_name"), source=d.get("source"), target=d.get("target"))


@dataclass
class Thresholds:
    column_name: str
    lower_bound: str
    upper_bound: str
    type: str

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> Thresholds:
        """Deserializes the Thresholds from a dictionary."""
        return cls(
            column_name=d.get("column_name"),
            lower_bound=d.get("lower_bound"),
            upper_bound=d.get("upper_bound"),
            type=d.get("type"),
        )


@dataclass
class Filters:
    source: str = None
    target: str = None

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> Filters:
        """Deserializes the Filters from a dictionary."""
        return cls(source=d.get("source"), target=d.get("target"))


@dataclass
class Tables:
    source_name: str
    target_name: str
    jdbc_reader_options: Optional[JdbcReaderOptions]
    join_columns: list[JoinColumns]
    select_columns: Optional[list[str]]
    drop_columns: Optional[list[str]]
    column_mapping: Optional[list[ColumnMapping]]
    transformations: Optional[list[Transformation]]
    thresholds: Optional[list[Thresholds]]
    filters: Optional[Filters]

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> Tables:
        """Deserializes the TableRecon from a dictionary."""
        return cls(
            source_name=d.get("source_name"),
            target_name=d.get("target_name"),
            jdbc_reader_options=_from_dict(d, "jdbc_reader_options", JdbcReaderOptions),
            join_columns=_repeated_dict(d, "join_columns", JoinColumns),
            select_columns=d.get("select_columns"),
            drop_columns=d.get("drop_columns"),
            column_mapping=_repeated_dict(d, "column_mapping", ColumnMapping),
            transformations=_repeated_dict(d, "transformations", Transformation),
            thresholds=_repeated_dict(d, "thresholds", Thresholds),
            filters=_from_dict(d, "filters", Filters),
        )

    def list_to_dict(self, cls: any, key: str) -> dict[str, any]:
        for _, value in self.__dict__.items():
            if isinstance(value, list):
                if all(isinstance(x, cls) for x in value):
                    return {getattr(v, key): v for v in value}
            else:
                pass


@dataclass
class TableRecon:
    source_catalog: Optional[str]
    source_schema: str
    target_catalog: str
    target_schema: str
    tables: list[Tables]

    @classmethod
    def from_dict(cls, d: dict[str, any]) -> TableRecon:
        """Deserializes the TableRecon from a dictionary."""
        return cls(
            source_catalog=d.get("source_catalog", None),
            source_schema=d.get("source_schema"),
            target_catalog=d.get("target_catalog"),
            target_schema=d.get("target_schema"),
            tables=_repeated_dict(d, "tables", Tables),
        )


@dataclass
class DatabaseConfig:
    source_catalog: Optional[str]
    source_schema: str
    target_catalog: str
    target_schema: str


@dataclass
class Schema:
    column_name: str
    data_type: str


@dataclass
class QueryConfig:
    table_transform: list[TransformRuleMapping]

    @classmethod
    def get_comparison_columns(cls, table_conf: Tables, schema: list[Schema]):
        cols_to_be_compared = []
        # get threshold columns
        if table_conf.thresholds:
            threshold_cols = [threshold.column_name for threshold in table_conf.thresholds]
        else:
            threshold_cols = []
        # explicit select columns
        if table_conf.select_columns:
            sel_cols = filter_list(input_list=table_conf.select_columns, remove_list=threshold_cols)
            join_cols = [join.source_name for join in table_conf.join_columns]
            cols_to_be_compared += (sel_cols + join_cols)
        # complete schema is considered here
        else:
            sel_cols = [schema.column_name for schema in schema]
            drop_cols = table_conf.drop_columns
            if drop_cols is None:
                drop_cols = []
            final_sel_cols = filter_list(input_list=sel_cols, remove_list=drop_cols + threshold_cols)
            cols_to_be_compared += final_sel_cols

        return cols_to_be_compared

    @classmethod
    def get_key_columns(cls, table_conf: Tables):
        key_columns = []
        if table_conf.join_columns:
            join_columns = [join.source_name for join in table_conf.join_columns]
            partition_column = table_conf.jdbc_reader_options.partition_column
            if partition_column not in join_columns:
                join_columns.append(partition_column)
            key_columns += join_columns

        return key_columns

    @classmethod
    def add_custom_transformations(cls, table_conf: Tables, cols: list[str], layer: str):
        transformation_dict = table_conf.list_to_dict(Transformation, "column_name")
        alias_mapping_dict = table_conf.list_to_dict(ColumnMapping, "source_name")

        if transformation_dict is not None:
            for col in cols:
                transformation_mapping = TransformRuleMapping(col, None, None)
                if alias_mapping_dict is not None and col in alias_mapping_dict.keys():
                    transformation_mapping.alias_name = alias_mapping_dict.get(col).target_name
                if transformation_dict is not None and col in transformation_dict.keys():
                    match layer:
                        case "source":
                            transformation_mapping.transformation = transformation_dict.get(col).source

                        case "target":
                            transformation_mapping.transformation = transformation_dict.get(col).target
                        case _:
                            print("Invalid layer value only source or target is allowed")
                else:
                    transformation_mapping = TransformRuleMapping(col, None, None)
                cls.table_transform.append(transformation_mapping)

        return cls

    @classmethod
    def generate_hash_algorithm(cls, source_type: str,
                                list_expr: list[str]) -> str:
        hash_expr = " || ".join(list_expr)
        hash_column = (Constants.hash_algorithm_mapping.get(source_type).get("source")).format(
            hash_expr)
        return hash_column

    def list_to_dict(self, cls: any, key: str) -> dict[str, any]:
        for _, value in self.__dict__.items():
            if isinstance(value, list):
                if all(isinstance(x, cls) for x in value):
                    return {getattr(v, key): v for v in value}
            else:
                pass

    def transform(self, func, *args, **kwargs) -> QueryConfig:
        result = func(self, *args, **kwargs)
        return result
