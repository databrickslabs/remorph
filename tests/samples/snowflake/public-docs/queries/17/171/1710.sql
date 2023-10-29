-- see https://docs.snowflake.com/en/sql-reference/transactions

SELECT query_id, query_text, start_time, session_id, execution_status, total_elapsed_time, compilation_time, execution_time
  FROM snowflake.account_usage.query_history
  WHERE transaction_id = '<transaction_id>';