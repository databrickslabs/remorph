-- see https://docs.snowflake.com/en/sql-reference/account-usage/lock_wait_history

SELECT query_id, object_name, transaction_id, blocker_queries
  FROM snowflake.account_usage.lock_wait_history
  WHERE requested_at >= dateadd('hours', -24, current_timestamp());