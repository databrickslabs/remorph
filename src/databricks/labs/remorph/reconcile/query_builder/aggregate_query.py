import logging
from itertools import groupby
from operator import attrgetter

import sqlglot.expressions as exp

from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    build_column,
)
from databricks.labs.remorph.reconcile.recon_config import Aggregate

logger = logging.getLogger(__name__)


class AggregateQueryBuilder(QueryBuilder):

    def _get_layer_query(self, group_list: list[Aggregate]) -> str:
        """
        Builds the query based on the  layer:
        * Creates an Expression using
            - 'select' columns with alias for the aggregate columns
            - 'filters' (where) based on the layer
            - 'group by' if group_by_cols are defined
        * Generates and returns the SQL query using the Expression
            and Dialect

        Examples:
        1.
           group_list: [Aggregate(type="Max", agg_cols=["col2", "col3"], group_by_cols=["col1"]),
                              Aggregate(type="Sum", agg_cols=["col1", "col2"], group_by_cols=["col1"])]
           :layer: "src"
           :returns -> SELECT max(col2) AS src_max_col2, max(col3) AS src_max_col3,
                                            sum(col1) AS src_sum_col1, sum(col2) AS src_sum_col2
                                FROM :tbl WHERE col1 IS NOT NULL GROUP BY col1
        2.
            group_list: [Aggregate(type="avg", agg_cols=["col4"])]
            :layer: "tgt"
            :returns -> SELECT avg(col4) AS tgt_avg_col4 FROM :tbl

        :param group_list: List of Aggregate objects with same Group by columns
        :return: SQL Query

        """
        cols_with_mapping: list[exp.Expression] = []
        # Generates a Single Query for multiple aggregates with the same group_by_cols,
        #   refer to Example 1
        for agg in group_list:
            print(f" - {agg}")
            for col in agg.agg_cols:
                # apply column mapping, ex: "{source: pid, target: product_id}"
                column_with_mapping = self.table_conf.get_layer_tgt_to_src_col_mapping(col, self.layer)
                if self.layer == "target":
                    column_with_mapping = self.table_conf.get_layer_src_to_tgt_col_mapping(col, self.layer)

                # create a Column Expression with agg_type+original column as alias, ex: "product_id AS max<#>pid"
                column_expr = build_column(this=f"{column_with_mapping}", alias=f"{agg.type}<#>{col}")

                cols_with_mapping.append(column_expr)

        # Apply user transformations if defined,
        # ex: {column_name: creation_date, source: creation_date, target: to_date(creation_date,'yyyy-mm-dd')}
        select_cols_with_transform = (
            self._apply_user_transformation(cols_with_mapping) if self.user_transformations else cols_with_mapping
        )

        cols_with_alias = []

        for transformed_col in select_cols_with_transform:
            # Split the alias defined above as agg_type(min, max etc..), original column (pid)
            agg_type, org_col_name = transformed_col.alias.split("<#>")

            # Create a new alias with layer, agg_type and original column name,
            # ex: source_min_pid, target_max_product_id
            layer_agg_type_col_alias = f"{self.layer}_{agg_type}_{org_col_name}".lower()

            # Get the Transformed column name without the alias
            col_name = transformed_col.sql().replace(f"AS {transformed_col.alias}", '').strip()

            # Create a new Column Expression with the new alias,
            # ex: MIN(pid) AS source_min_pid, MIN(product_id) AS target_min_pid
            col_with_alias = build_column(this=f"{agg_type.upper()}({col_name})",
                                          alias=layer_agg_type_col_alias)
            cols_with_alias.append(col_with_alias)

        query_exp = (
            exp.select(*cols_with_alias)
            .from_(":tbl")
            .where(self.filter)
        )

        # Apply Group by if group_by_cols are defined
        if group_list[0].group_by_cols:
            group_by_cols_with_alias = [build_column(this=col) for col in group_list[0].group_by_cols]

            # Apply user transformations on group_by_cols,
            # ex: {column_name: creation_date, source: creation_date, target: to_date(creation_date,'yyyy-mm-dd')}
            group_by_cols_with_transform = (
                self._apply_user_transformation(group_by_cols_with_alias) if self.user_transformations
                else group_by_cols_with_alias
            )
            query_exp = (exp.select(*cols_with_alias + group_by_cols_with_transform)
                         .from_(":tbl")
                         .where(self.filter)
                         .group_by(*group_by_cols_with_transform))

        print(f" - Query Expression: {query_exp}")
        return query_exp.sql(dialect=self.engine)

    def grouped_aggregates(self):
        """
            Group items based on group_by_cols_keys:
            Example:
              aggregates = [
                                        Aggregate(type="Min", agg_cols=["c_nation_str", "col2"],
                                                                                        group_by_cols=["col3"]),
                                        Aggregate(type="Max", agg_cols=["col2", "col3"], group_by_cols=["col1"]),
                                        Aggregate(type="avg", agg_cols=["col4"]),
                                        Aggregate(type="sum", agg_cols=["col3", "col6"], group_by_cols=["col1"]),
                                    ]
              output:
                      * key: NA with index 1
                        - Aggregate(agg_cols=['col4'], type='avg', group_by_cols=None, group_by_cols_as_str='NA')
                      * key: col1 with index 2
                        - Aggregate(agg_cols=['col2', 'col3'], type='Max', group_by_cols=['col1'],
                                                                                      group_by_cols_as_str='col1')
                        - Aggregate(agg_cols=['col3', 'col6'], type='sum', group_by_cols=['col1'],
                                                                                       group_by_cols_as_str='col1')
                      * key: col3 with index 3
                        - Aggregate(agg_cols=['c_nation_str', 'col2'], type='Min', group_by_cols=['col3'],
                        group_by_cols_as_str='col3')
        """
        _aggregates: list[Aggregate] = []

        assert self.aggregates, "Aggregates config must be defined to build the queries."
        if self.aggregates:
            _aggregates = self.aggregates

        # Sort the aggregates based on group_by_cols_as_str
        _aggregates.sort(key=attrgetter("group_by_cols_as_str"))

        return groupby(_aggregates, key=attrgetter("group_by_cols_as_str"))

    def build_queries(self) -> dict[str, str]:
        """
        Generates the Source and Target Queries for the list of Aggregate objects
        * Group items based on group_by_cols_keys and for each group,
            generates the query for both Source and Target Dialects
        * Generates 2 Queries (Source, Target) for each unique group_by_cols_keys

        Examples:
        1. [Aggregate(type="avg", agg_cols=["col4"])]
            {
            "src_query_1": "SELECT avg(col4) AS src_avg_col4 FROM :tbl"
            }
            {
            "tgt_query_1": "SELECT avg(col4) AS tgt_avg_col4 FROM :tbl"
            }
         2. [Aggregate(type="Max", agg_cols=["col3"], group_by_cols=["col1"]),
              Aggregate(type="Sum", agg_cols=["col2"], group_by_cols=["col4"])]
            {
            "src_query_1": "SELECT max(col3) AS src_max_col3 FROM :tbl GROUP BY col1"
            "src_query_2": "SELECT sum(col2) AS src_sum_col2 FROM :tbl GROUP BY col4"
            }
            {
            "tgt_query_1": "SELECT max(col3) AS tgt_max_col3 FROM :tbl GROUP BY col1"
            "tgt_query_2": "SELECT sum(col2) AS tgt_sum_col2 FROM :tbl GROUP BY col4"
            }
        :return: Dictionary with Source and Target Queries
        """

        queries_dict = {}
        for index, (key, group) in enumerate(self.grouped_aggregates(), start=1):
            # print(f"{key}: {list(group)}")
            print(f"key: {key} with index {index}")

            group_list: list[Aggregate] = list(group)

            query = self._get_layer_query(group_list)
            logger.info(f"Aggregate Query for {self.layer} {group_list[0].group_by_cols_as_str} {index}: {query}")
            queries_dict[f"{self.layer}_query_{index}"] = query

        return queries_dict
