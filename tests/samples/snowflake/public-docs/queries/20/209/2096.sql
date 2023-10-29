-- see https://docs.snowflake.com/en/sql-reference/functions/materialized_view_refresh_history

select *
  from table(information_schema.materialized_view_refresh_history(
    date_range_start=>dateadd(D, -7, current_date),
    date_range_end=>current_date));