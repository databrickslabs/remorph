-- see https://docs.snowflake.com/en/sql-reference/account-usage/complete_task_graphs

select root_task_name, state from snowflake.account_usage.complete_task_graphs
  limit 10;