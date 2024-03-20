from io import StringIO

from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import (
    ColumnTransformationType,
    Constants,
    SourceType,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    Tables,
    Transformation,
    TransformRuleMapping,
)


class QueryBuilder:

    def __init__(self, table_conf: Tables, schema: list[Schema], layer: str, source: str):
        self.table_conf = table_conf
        self.schema = schema
        self.layer = layer
        self.source = source

    def build_hash_query(self) -> str:
        schema_info = {v.column_name: v for v in self.schema}

        columns, key_columns = self._get_column_list()
        col_transformations = self._generate_transformation_rule_mapping(columns, schema_info)

        hash_columns_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expression_without_alias, col_transformations)
        )
        hash_expr = self._generate_hash_algorithm(self.source, hash_columns_expr)

        key_column_transformation = self._generate_transformation_rule_mapping(key_columns, schema_info)
        key_column_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expression_with_alias, key_column_transformation)
        )

        if self.layer == "source":
            table_name = self.table_conf.source_name
            query_filter = self.table_conf.filters.source if self.table_conf.filters else " 1 = 1 "
        else:
            table_name = self.table_conf.target_name
            query_filter = self.table_conf.filters.target if self.table_conf.filters else " 1 = 1 "

        # construct select query
        select_query = self._construct_hash_query(table_name, query_filter, hash_expr, key_column_expr)

        return select_query

    def _get_column_list(self) -> tuple[list[str], list[str]]:
        tgt_column_mapping = self.table_conf.list_to_dict(ColumnMapping, "target_name")

        if self.table_conf.join_columns is None:
            join_columns = set()
        else:
            join_columns = set(self.table_conf.join_columns)

        if self.table_conf.select_columns is None:
            columns = {sch.column_name for sch in self.schema}
            select_columns = (
                columns if self.layer == "source" else self._get_mapped_columns(tgt_column_mapping, columns)
            )
        else:
            select_columns = set(self.table_conf.select_columns)

        if self.table_conf.jdbc_reader_options and self.layer == "source":
            partition_column = {self.table_conf.jdbc_reader_options.partition_column}
        else:
            partition_column = set()

        # Combine all column names
        all_columns = join_columns | select_columns

        # Remove threshold and drop columns
        threshold_columns = {thresh.column_name for thresh in self.table_conf.thresholds or []}
        if self.table_conf.drop_columns is None:
            drop_columns = set()
        else:
            drop_columns = set(self.table_conf.drop_columns)

        columns = sorted(all_columns - threshold_columns - drop_columns)
        key_columns = sorted(join_columns | partition_column)

        return columns, key_columns

    def _generate_transformation_rule_mapping(self, columns: list[str], schema: dict) -> list[TransformRuleMapping]:
        transformations_dict = self.table_conf.list_to_dict(Transformation, "column_name")
        column_mapping_dict = self.table_conf.list_to_dict(ColumnMapping, "source_name")

        if transformations_dict:
            columns_with_transformation = [column for column in columns if column in transformations_dict.keys()]
            custom_transformation = self._get_custom_transformation(
                columns_with_transformation, transformations_dict, column_mapping_dict
            )
        else:
            custom_transformation = []

        columns_without_transformation = [column for column in columns if column not in transformations_dict.keys()]
        default_transformation = self._get_default_transformation(
            columns_without_transformation, column_mapping_dict, schema
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
    def _generate_hash_algorithm(source: str, column_expr: list[str]) -> str:
        if source in {SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value}:
            hash_expr = "concat(" + ", ".join(column_expr) + ")"
        else:
            hash_expr = " || ".join(column_expr)

        return (Constants.hash_algorithm_mapping.get(source.lower()).get("source")).format(hash_expr)

    @staticmethod
    def _construct_hash_query(table_name: str, query_filter: str, hash_expr: str, key_column_expr: list[str]) -> str:
        sql_query = StringIO()
        sql_query.write(f"select {hash_expr} as {Constants.hash_column_name}")

        # add join column
        if key_column_expr:
            sql_query.write(", " + ",".join(key_column_expr))
        sql_query.write(f" from {table_name} where {query_filter}")

        select_query = sql_query.getvalue()
        sql_query.close()
        return select_query

    @staticmethod
    def _get_mapped_columns(column_mapping: dict, columns: set[str]) -> set[str]:
        select_columns = set()
        for column in columns:
            select_columns.add(column_mapping.get(column).source_name if column_mapping.get(column) else column)
        return select_columns

    @staticmethod
    def _get_column_map(column, column_mapping) -> str:
        return column_mapping.get(column).target_name if column_mapping.get(column) else column

    def _get_custom_transformation(self, columns, transformation_dict, column_mapping):
        transformation_rule_mapping = []
        for column in columns:
            if column in transformation_dict.keys():
                transformation = self._get_layer_transform(transformation_dict, column, self.layer)
            else:
                transformation = None

            column_origin, column_alias = self._get_column_alias(self.layer, column, column_mapping)

            transformation_rule_mapping.append(TransformRuleMapping(column_origin, transformation, column_alias))

        return transformation_rule_mapping

    def _get_default_transformation(self, columns, column_mapping, schema):
        transformation_rule_mapping = []
        for column in columns:
            column_origin = column if self.layer == "source" else self._get_column_map(column, column_mapping)
            column_data_type = schema.get(column_origin).data_type
            transformation = self._get_default_transformation_mapping(self.source, column_data_type).format(
                column_origin
            )

            column_origin, column_alias = self._get_column_alias(self.layer, column, column_mapping)

            transformation_rule_mapping.append(TransformRuleMapping(column_origin, transformation, column_alias))

        return transformation_rule_mapping

    @staticmethod
    def _get_default_transformation_mapping(data_source: str, data_type: str) -> str:
        if data_source == "oracle":
            return OracleDataSource.oracle_datatype_mapper.get(data_type, ColumnTransformationType.ORACLE_DEFAULT.value)
        if data_source == "snowflake":
            return SnowflakeDataSource.snowflake_datatype_mapper.get(
                data_type, ColumnTransformationType.SNOWFLAKE_DEFAULT.value
            )
        if data_source == "databricks":
            return DatabricksDataSource.databricks_datatype_mapper.get(
                data_type, ColumnTransformationType.DATABRICKS_DEFAULT.value
            )
        msg = f"Unsupported source type --> {data_source}"
        raise ValueError(msg)

    @staticmethod
    def _get_column_alias(layer, column, column_mapping):
        if column_mapping and column in column_mapping.keys() and layer == "target":
            column_alias = column_mapping.get(column).source_name
            column_origin = column_mapping.get(column).target_name
        else:
            column_alias = column
            column_origin = column

        return column_origin, column_alias

    def build_threshold_query(self) -> str:
        column_mapping = self.table_conf.list_to_dict(ColumnMapping, "source_name")
        transformations_dict = self.table_conf.list_to_dict(Transformation, "column_name")

        threshold_columns = set(threshold.column_name for threshold in self.table_conf.thresholds)
        join_columns = set(self.table_conf.join_columns)

        if self.table_conf.jdbc_reader_options and self.layer == "source":
            partition_column = {self.table_conf.jdbc_reader_options.partition_column}
        else:
            partition_column = set()

        all_columns = set(threshold_columns | join_columns | partition_column)

        query_columns = sorted(
            all_columns if self.layer == "source" else self._get_mapped_columns(column_mapping, all_columns)
        )

        transformation_rule_mapping = self._get_custom_transformation(
            query_columns, transformations_dict, column_mapping
        )
        threshold_columns_expr = self._get_column_expr(
            TransformRuleMapping.get_column_expression_with_alias, transformation_rule_mapping
        )

        if self.layer == "source":
            table_name = self.table_conf.source_name
            query_filter = self.table_conf.filters.source if self.table_conf.filters else " 1 = 1 "
        else:
            table_name = self.table_conf.target_name
            query_filter = self.table_conf.filters.target if self.table_conf.filters else " 1 = 1 "

        # construct threshold select query
        select_query = self._construct_threshold_query(table_name, query_filter, threshold_columns_expr)

        return select_query

    @staticmethod
    def _construct_threshold_query(table_name, query_filter, threshold_columns_expr):
        sql_query = StringIO()
        column_expr = ",".join(threshold_columns_expr)
        sql_query.write(f"select {column_expr} ")

        sql_query.write(f" from {table_name} where {query_filter}")

        select_query = sql_query.getvalue()
        sql_query.close()
        return select_query
