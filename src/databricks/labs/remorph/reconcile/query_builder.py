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
    Schema,
    Transformation,
    TransformRuleMapping,
)


class QueryBuilder(ABC):

    def __init__(self, qrc: QueryConfig):
        self.qrc = qrc

    @abstractmethod
    def build_query(self):
        raise NotImplementedError

    def _get_custom_transformation(
        self, cols: list[str], transform_dict: dict[str, Transformation], col_mapping: dict[str, ColumnMapping]
    ) -> list[TransformRuleMapping]:
        transform_rule_mapping = []
        for col in cols:
            if col in transform_dict.keys():
                transform = self._get_layer_transform(transform_dict, col, self.qrc.layer)
            else:
                transform = None

            col_origin, col_alias = self._get_column_alias(self.qrc.layer, col, col_mapping)

            transform_rule_mapping.append(TransformRuleMapping(col_origin, transform, col_alias))

        return transform_rule_mapping

    def _get_default_transformation(
        self, cols: list[str], col_mapping: dict[str, ColumnMapping], schema: dict[str, Schema]
    ) -> list[TransformRuleMapping]:
        transform_rule_mapping = []
        for col in cols:
            col_origin = col if self.qrc.layer == "source" else self._get_column_map(col, col_mapping)
            col_data_type = schema.get(col_origin).data_type
            transform = self._get_default_transformation_expr(self.qrc.source, col_data_type).format(col_origin)

            col_origin, col_alias = self._get_column_alias(self.qrc.layer, col, col_mapping)

            transform_rule_mapping.append(TransformRuleMapping(col_origin, transform, col_alias))

        return transform_rule_mapping

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

    def _generate_transform_rule_mapping(self, cols: list[str]) -> list[TransformRuleMapping]:

        # compute custom transformation
        if self.qrc.transform_dict:
            cols_with_transform = [col for col in cols if col in self.qrc.transform_dict.keys()]
            custom_transform = self._get_custom_transformation(
                cols_with_transform, self.qrc.transform_dict, self.qrc.src_col_mapping
            )
        else:
            custom_transform = []

        # compute default transformation
        cols_without_transform = [col for col in cols if col not in self.qrc.transform_dict.keys()]
        default_transform = self._get_default_transformation(
            cols_without_transform, self.qrc.src_col_mapping, self.qrc.schema_dict
        )

        transform_rule_mapping = custom_transform + default_transform

        return transform_rule_mapping

    @staticmethod
    def _get_layer_transform(transform_dict: dict[str, Transformation], col: str, layer: str) -> str:
        return transform_dict.get(col).source if layer == "source" else transform_dict.get(col).target

    @staticmethod
    def _get_column_expr(func, col_transform: list[TransformRuleMapping]):
        return [func(transform) for transform in col_transform]

    @staticmethod
    def _get_column_map(col, col_mapping: dict[str, ColumnMapping]) -> str:
        return col_mapping.get(col, ColumnMapping(source_name='', target_name=col)).target_name

    @staticmethod
    def _get_column_alias(layer: str, col: str, col_mapping: dict[str, ColumnMapping]) -> tuple[str, str]:
        if col_mapping and col in col_mapping.keys() and layer == "target":
            col_alias = col_mapping.get(col).source_name
            col_origin = col_mapping.get(col).target_name
        else:
            col_alias = col
            col_origin = col

        return col_origin, col_alias


class HashQueryBuilder(QueryBuilder):

    def build_query(self) -> str:
        hash_cols = sorted(
            (self.qrc.join_columns | self.qrc.select_columns) - self.qrc.threshold_columns - self.qrc.drop_columns
        )
        key_cols = sorted(self.qrc.join_columns | self.qrc.partition_column)

        # get transformation for columns considered for hashing
        col_transform = self._generate_transform_rule_mapping(hash_cols)
        hash_cols_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expr_without_alias, col_transform)
        )
        hash_expr = self._generate_hash_algorithm(self.qrc.source, hash_cols_expr)

        # get transformation for columns considered for joining and partition key
        key_col_transform = self._generate_transform_rule_mapping(key_cols)
        key_col_expr = sorted(self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, key_col_transform))

        # construct select hash query
        select_query = self._construct_hash_query(self.qrc.table_name, self.qrc.filter, hash_expr, key_col_expr)

        return select_query

    @staticmethod
    def _generate_hash_algorithm(source: str, col_expr: list[str]) -> str:
        if source in {SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value}:
            hash_expr = "concat(" + ", ".join(col_expr) + ")"
        else:
            hash_expr = " || ".join(col_expr)

        return (Constants.hash_algorithm_mapping.get(source).get("source")).format(hash_expr)

    @staticmethod
    def _construct_hash_query(table: str, query_filter: str, hash_expr: str, key_col_expr: list[str]) -> str:
        sql_query = StringIO()
        # construct hash expr
        sql_query.write(f"select {hash_expr} as {Constants.hash_column_name}")

        # add join column
        if key_col_expr:
            sql_query.write(", " + ",".join(key_col_expr))
        sql_query.write(f" from {table} where {query_filter}")

        select_query = sql_query.getvalue()
        sql_query.close()
        return select_query


class ThresholdQueryBuilder(QueryBuilder):

    def build_query(self) -> str:
        all_columns = set(self.qrc.threshold_columns | self.qrc.join_columns | self.qrc.partition_column)

        query_columns = sorted(
            all_columns
            if self.qrc.layer == "source"
            else self.qrc.get_mapped_columns(self.qrc.src_col_mapping, all_columns)
        )

        transform_rule_mapping = self._get_custom_transformation(
            query_columns, self.qrc.transform_dict, self.qrc.src_col_mapping
        )
        col_expr = self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, transform_rule_mapping)

        select_query = self._construct_threshold_query(self.qrc.table_name, self.qrc.filter, col_expr)

        return select_query

    @staticmethod
    def _construct_threshold_query(table, query_filter, col_expr) -> str:
        expr = ",".join(col_expr)
        return f"select {expr} from {table} where {query_filter}"
