import logging

from databricks.labs.remorph.reconcile.constants import ThresholdMode
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Table, TransformRuleMapping

logger = logging.getLogger(__name__)


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

    # Comparison query
    def build_comparison_query(self) -> str:
        threshold_columns = sorted(set(self.table_conf.get_threshold_columns))
        join_columns = sorted(set(self.table_conf.get_join_columns))
        # generate select clause and where clause
        select_clause, where_clause = self._generate_select_where_clause(threshold_columns)
        # add join columns to select clause
        select_clause.extend([f"source.{column} as {column}" for column in join_columns])
        # generate join condition dynamically
        join_condition = self._get_join_condition(join_columns)
        # construct the final query
        comparison_query = self._construct_comparison_query(
            self.table_conf, select_clause, join_condition, where_clause
        )

        logger.info(f"Comparison Query: {comparison_query}")
        print(f"Comparison Query: {comparison_query}")
        return comparison_query

    def _generate_select_where_clause(self, threshold_columns: set[str]) -> (list[str], list[str]):
        select_clause = []
        where_clause = []
        for column in threshold_columns:
            # get the user provided threshold details at column level
            threshold = self._get_threshold_info(column)
            # check if the threshold is in percentage or absolute mode
            mode = (
                ThresholdMode.PERCENTILE.value
                if "%" in threshold.lower_bound or "%" in threshold.upper_bound
                else ThresholdMode.ABSOLUTE.value
            )
            # Use the dictionary to get the corresponding function
            select_clause.append(
                self._get_threshold_select_function(threshold.type, mode).format(
                    column=column,
                    lower_bound=threshold.lower_bound.replace("%", ""),
                    upper_bound=threshold.upper_bound.replace("%", ""),
                )
            )
            # where clause generation
            where_clause.append(self._get_threshold_filter_function(threshold.type).format(column=column))
        return select_clause, where_clause

    @staticmethod
    def _construct_comparison_query(
        table_conf: Table, select_clause: list[str], join_condition: str, where_clause: list[str]
    ) -> str:
        select_text = ", ".join(select_clause)
        where_text = " or ".join(where_clause)
        source_view = f"{table_conf.source_name}_df_threshold_vw"
        target_view = f"{table_conf.target_name}_df_threshold_vw"
        select_query = f"""select {select_text}
        from {source_view} source inner join 
        {target_view} databricks on {join_condition}
        where {where_text} """.strip()

        return select_query
