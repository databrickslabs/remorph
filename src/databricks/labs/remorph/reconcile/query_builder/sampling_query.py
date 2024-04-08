from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import TransformRuleMapping


class SamplingQueryBuilder(QueryBuilder):

    def build_query(self, df: DataFrame):
        key_cols = sorted(self.table_conf.join_columns)
        keys_df = df.select(*key_cols)
        with_clause = self._get_with_clause(keys_df, self.source)

        cols = sorted(
            (self.table_conf.join_columns | self.select_columns)
            - self.table_conf.threshold_columns
            - self.table_conf.drop_columns
        )

        col_transform = self._generate_transform_rule_mapping(cols)
        cols_expr = sorted(self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, col_transform))

        query_filter = self.table_conf.get_filter(self.layer)
        select_query = self._construct_query(self.table_name, query_filter, cols_expr, with_clause, key_cols)
        return select_query

    @staticmethod
    def _construct_query(
        table: str, query_filter: str, col_expr: list[str], with_clause: str, key_cols: list[str]
    ) -> str:

        where = f"where {query_filter}" if query_filter else ''
        with_cte = f"{with_clause} src as ( select " + ",".join(col_expr) + f" from {table} {where})"

        if not key_cols:
            raise AssertionError("key cols cannot be empty")

        join_expr = [f"recon.{col} = src.{col}" for col in key_cols]
        join_condition = " and ".join(join_expr)
        join = f" select src.* from src join recon on {join_condition}"

        select_query = with_cte + join
        return select_query

    @staticmethod
    def _get_with_clause(df: DataFrame, source: str):
        select_clause = []
        for row in df.take(50):
            row_select = "select " + ", ".join(
                [
                    f"'{value}' as {column}" if value is not None else f"null as {column}"
                    for column, value in zip(df.columns, row)
                ]
            )
            # Remove the trailing comma and add 'union'
            if source == SourceType.ORACLE.value:
                row_select += " from dual"
            select_clause.append(row_select)

        return "with recon as (" + ' union \n'.join(select_clause) + "),"
