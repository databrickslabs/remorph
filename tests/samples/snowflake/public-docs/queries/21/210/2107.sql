-- see https://docs.snowflake.com/en/sql-reference/functions/replication_usage_history

select *
  from table(information_schema.replication_usage_history(
    date_range_start=>dateadd(d, -7, current_date),
    date_range_end=>current_date,
    database_name=>'mydb'));