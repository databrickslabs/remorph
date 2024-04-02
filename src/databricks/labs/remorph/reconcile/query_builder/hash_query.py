from io import StringIO

from databricks.labs.remorph.reconcile.constants import Constants, SourceType
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import TransformRuleMapping


class HashQueryBuilder(QueryBuilder):

    def build_query(self) -> str:
        hash_cols = sorted(
            (self.table_conf.get_join_columns | self.select_columns)
            - self.table_conf.get_threshold_columns
            - self.table_conf.get_drop_columns
        )
        key_cols = sorted(self.table_conf.get_join_columns | self.table_conf.get_partition_column(self.layer))

        # get transformation for columns considered for hashing
        col_transform = self._generate_transform_rule_mapping(hash_cols)
        hash_cols_expr = sorted(
            self._get_column_expr(TransformRuleMapping.get_column_expr_without_alias, col_transform)
        )
        hash_expr = self._generate_hash_algorithm(self.source, hash_cols_expr)

        # get transformation for columns considered for joining and partition key
        key_col_transform = self._generate_transform_rule_mapping(key_cols)
        key_col_expr = sorted(self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, key_col_transform))

        # construct select hash query
        select_query = self._construct_hash_query(
            self.table_name, self.table_conf.get_filter(self.layer), hash_expr, key_col_expr
        )

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
