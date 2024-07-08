import logging
from itertools import groupby

import sqlglot.expressions as exp

from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    build_column,
)

logger = logging.getLogger(__name__)


class AggregateQueryBuilder(QueryBuilder):

    def build_query(self) -> list[str]:

        queries: list[str] = []

        self.aggregates.sort(key=lambda agg: agg.group_by_cols_keys)

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
                      * key: NA
                        - Aggregate(agg_cols=['col4'], type='avg', group_by_cols=None, group_by_cols_as_str='NA')
                      * key: col1
                        - Aggregate(agg_cols=['col2', 'col3'], type='Max', group_by_cols=['col1'], 
                                                                                      group_by_cols_as_str='col1')
                        - Aggregate(agg_cols=['col3', 'col6'], type='sum', group_by_cols=['col1'], 
                                                                                       group_by_cols_as_str='col1')
                      * key: col3
                        - Aggregate(agg_cols=['c_nation_str', 'col2'], type='Min', group_by_cols=['col3'], 
                        group_by_cols_as_str='col3')   
        """
        grouped_items = groupby(self.aggregates, key=lambda agg: agg.group_by_cols_keys)

        for key, group in grouped_items:
            # print(f"{key}: {list(group)}")
            print(f"key: {key}")
            cols_with_alias: list[exp.Expression] = []
            for agg in group:
                print(f" - {agg}")
                cols_with_alias.extend([
                    build_column(this=col, alias=f"{self.layer}_{agg.type}_{col}")
                    for col in agg.agg_cols
                ])

            query = (exp.select(*cols_with_alias)
                     .from_(":tbl")
                     .where(self.filter)
                     .group_by(*group[0].group_by_cols)
                     .sql(dialect=self.source))

            logger.info(f"Aggregate Query for {self.layer} {group[0].group_by_cols_as_str}: {query}")
            queries.append(
                query
            )

        return queries
