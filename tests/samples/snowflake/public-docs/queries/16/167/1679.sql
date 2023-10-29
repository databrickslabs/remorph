-- see https://docs.snowflake.com/en/sql-reference/account-usage/alert_history

SELECT name, condition, condition_query_id, action, action_query_id, state
FROM snowflake.account_usage.alert_history
LIMIT 10;