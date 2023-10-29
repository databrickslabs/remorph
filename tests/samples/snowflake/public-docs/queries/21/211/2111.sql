-- see https://docs.snowflake.com/en/sql-reference/functions/search_optimization_history

select *
  from table(information_schema.search_optimization_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));