-- see https://docs.snowflake.com/en/sql-reference/functions/database_replication_usage_history

select start_time, end_time, database_name, credits_used, bytes_transferred
  from table(information_schema.database_replication_usage_history(
    date_range_start=>dateadd(d, -7, current_date),
    date_range_end=>current_date,
    database_name=>'mydb'));