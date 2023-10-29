-- see https://docs.snowflake.com/en/sql-reference/functions/system_estimate_search_optimization_costs

SELECT SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS('table_without_search_opt', 'EQUALITY(C1, C2, C3)')
  AS estimate_for_columns_without_search_optimization;