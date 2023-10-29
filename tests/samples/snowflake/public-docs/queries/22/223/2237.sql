-- see https://docs.snowflake.com/en/sql-reference/account-usage/copy_history

select file_name, error_count, status, last_load_time from snowflake.account_usage.copy_history
  order by last_load_time desc
  limit 10;