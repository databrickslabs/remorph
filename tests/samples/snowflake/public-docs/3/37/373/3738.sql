SELECT file_name, last_load_time FROM snowflake.account_usage.load_history
  ORDER BY last_load_time DESC
  LIMIT 10;