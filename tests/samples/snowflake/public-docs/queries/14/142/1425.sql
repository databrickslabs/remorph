-- see https://docs.snowflake.com/en/sql-reference/functions/system_estimate_search_optimization_costs

SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_without_search_opt')
  AS estimate_for_table_without_search_optimization;