from abc import ABC, abstractmethod
from io import StringIO

from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import (
    ColumnTransformationType,
    Constants,
    SourceType,
)
from databricks.labs.remorph.reconcile.query_config import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Transformation,
    TransformRuleMapping,
)

# pylint: disable=invalid-name


class QueryBuilder(ABC):

    def __init__(self, qc: QueryConfig):
        self.qc = qc

    @abstractmethod
    def build_query(self):
        raise NotImplementedError

    def _get_custom_transformation(self, columns, transformation_dict, column_mapping):
        transformation_rule_mapping = []
        for column in columns:
            if column in transformation_dict.keys():
                transformation = self._get_layer_transform(transformation_dict, column, self.qc.layer)
            else:
                transformation = None

            column_origin, column_alias = self._get_column_alias(self.qc.layer, column, column_mapping)

            transformation_rule_mapping.append(TransformRuleMapping(column_origin, transformation, column_alias))

        return transformation_rule_mapping

    def _get_default_transformation(self, columns, column_mapping, schema):
        transformation_rule_mapping = []
        for column in columns:
            column_origin = column if self.qc.layer == "source" else self._get_column_map(column, column_mapping)
            column_data_type = schema.get(column_origin).data_type
            transformation = self._get_default_transformation_expr(self.qc.db_type, column_data_type).format(
                column_origin
            )

            column_origin, column_alias = self._get_column_alias(self.qc.layer, column, column_mapping)

            transformation_rule_mapping.append(TransformRuleMapping(column_origin, transformation, column_alias))

        return transformation_rule_mapping

    @staticmethod
    def _get_default_transformation_expr(data_source: str, data_type: str) -> str:
        if data_source == SourceType.ORACLE.value:
            return OracleDataSource.oracle_datatype_mapper.get(data_type, ColumnTransformationType.ORACLE_DEFAULT.value)
        if data_source == SourceType.SNOWFLAKE.value:
            return SnowflakeDataSource.snowflake_datatype_mapper.get(
                data_type, ColumnTransformationType.SNOWFLAKE_DEFAULT.value
            )
        if data_source == SourceType.DATABRICKS.value:
            return DatabricksDataSource.databricks_datatype_mapper.get(
                data_type, ColumnTransformationType.DATABRICKS_DEFAULT.value
            )
        msg = f"Unsupported source type --> {data_source}"
        raise ValueError(msg)

    def _generate_transformation_rule_mapping(self, columns: list[str]) -> list[TransformRuleMapping]:

        # compute custom transformation
        if self.qc.transformations_dict:
            columns_with_transformation = [
                column for column in columns if column in self.qc.transformations_dict.keys()
            ]
            custom_transformation = self._get_custom_transformation(
                columns_with_transformation, self.qc.transformations_dict, self.qc.src_column_mapping
            )
        else:
            custom_transformation = []

        # compute default transformation
        columns_without_transformation = [
            column for column in columns if column not in self.qc.transformations_dict.keys()
        ]
        default_transformation = self._get_default_transformation(
            columns_without_transformation, self.qc.src_column_mapping, self.qc.schema_dict
        )

        transformation_rule_mapping = custom_transformation + default_transformation

        return transformation_rule_mapping

    @staticmethod
    def _get_layer_transform(transform_dict: dict[str, Transformation], column: str, layer: str) -> str:
        return transform_dict.get(column).source if layer == "source" else transform_dict.get(column).target

    @staticmethod
    def _get_column_expr(func, column_transformations: list[TransformRuleMapping]):
        return [func(transformation) for transformation in column_transformations]

    @staticmethod
    def _get_column_map(column, column_mapping) -> str:
        return column_mapping.get(column, ColumnMapping(source_name='', target_name=column)).target_name

    @staticmethod
    def _get_column_alias(layer, column, column_mapping):
        if column_mapping and column in column_mapping.keys() and layer == "target":
            column_alias = column_mapping.get(column).source_name
            column_origin = column_mapping.get(column).target_name
        else:
            column_alias = column
            column_origin = column

        return column_origin, column_alias


class HashQueryBuilder(QueryBuilder):

    def build_query(self):
        columns = sorted(
            (self.qc.get_join_columns() | self.qc.get_select_columns())
            - self.qc.get_threshold_columns()
            - self.qc.get_drop_columns()
        )
        key_columns = sorted(self.qc.get_join_columns() | self.qc.get_partition_column())

        # get transformation for columns considered for hashing
        col_transformations = self._generate_transformation_rule_mapping(columns)
        hash_columns_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expression_without_alias, col_transformations)
        )
        hash_expr = self._generate_hash_algorithm(self.qc.db_type, hash_columns_expr)

        # get transformation for columns considered for joining and partition key
        key_column_transformation = self._generate_transformation_rule_mapping(key_columns)
        key_column_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expression_with_alias, key_column_transformation)
        )

        # construct select hash query
        select_query = self._construct_hash_query(
            self.qc.get_table_name(), self.qc.get_filter(), hash_expr, key_column_expr
        )

        return select_query

    @staticmethod
    def _generate_hash_algorithm(source: str, column_expr: list[str]) -> str:
        if source in {SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value}:
            hash_expr = "concat(" + ", ".join(column_expr) + ")"
        else:
            hash_expr = " || ".join(column_expr)

        return (Constants.hash_algorithm_mapping.get(source.lower()).get("source")).format(hash_expr)

    @staticmethod
    def _construct_hash_query(table_name: str, query_filter: str, hash_expr: str, key_column_expr: list[str]) -> str:
        sql_query = StringIO()
        # construct hash expr
        sql_query.write(f"select {hash_expr} as {Constants.hash_column_name}")

        # add join column
        if key_column_expr:
            sql_query.write(", " + ",".join(key_column_expr))
        sql_query.write(f" from {table_name} where {query_filter}")

        select_query = sql_query.getvalue()
        sql_query.close()
        return select_query


class ThresholdQueryBuilder(QueryBuilder):

    def build_query(self):
        all_columns = set(self.qc.get_threshold_columns() | self.qc.get_join_columns() | self.qc.get_partition_column())

        query_columns = sorted(
            all_columns
            if self.qc.layer == "source"
            else self.qc.get_mapped_columns(self.qc.src_column_mapping, all_columns)
        )

        transformation_rule_mapping = self._get_custom_transformation(
            query_columns, self.qc.transformations_dict, self.qc.src_column_mapping
        )
        threshold_columns_expr = self._get_column_expr(
            TransformRuleMapping.get_column_expression_with_alias, transformation_rule_mapping
        )

        select_query = self._construct_threshold_query(
            self.qc.get_table_name(), self.qc.get_filter(), threshold_columns_expr
        )

        return select_query

    @staticmethod
    def _construct_threshold_query(table_name, query_filter, threshold_columns_expr):
        column_expr = ",".join(threshold_columns_expr)
        return f"select {column_expr} from {table_name} where {query_filter}"
