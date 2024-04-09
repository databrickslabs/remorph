from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import TransformRuleMapping


class ThresholdQueryBuilder(QueryBuilder):
    def build_query(self) -> str:
        all_columns = set(
            self.table_conf.get_threshold_columns
            | self.table_conf.get_join_columns
            | self.table_conf.get_partition_column(self.layer)
        )

        query_columns = sorted(
            all_columns if self.layer == "source" else self._get_mapped_columns(self.src_col_mapping, all_columns)
        )

        transform_rule_mapping = self._get_custom_transformation(
            query_columns, self.transform_dict, self.src_col_mapping
        )
        col_expr = self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, transform_rule_mapping)

        select_query = self._construct_threshold_query(
            self.table_name, self.table_conf.get_filter(self.layer), col_expr
        )

        return select_query

    @staticmethod
    def _construct_threshold_query(table, query_filter, col_expr) -> str:
        expr = ",".join(col_expr)
        return f"select {expr} from {table} where {query_filter}"
