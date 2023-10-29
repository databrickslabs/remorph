-- see https://docs.snowflake.com/en/sql-reference/transactions

SELECT object_name, lock_type, transaction_id, blocker_queries
  FROM snowflake.account_usage.lock_wait_history
  WHERE query_id = '<query_id>';