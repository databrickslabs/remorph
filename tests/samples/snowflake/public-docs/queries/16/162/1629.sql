-- see https://docs.snowflake.com/en/sql-reference/account-usage/load_history

SELECT file_name, last_load_time FROM snowflake.account_usage.load_history
  ORDER BY last_load_time DESC
  LIMIT 10;