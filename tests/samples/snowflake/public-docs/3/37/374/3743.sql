SELECT name, condition, condition_query_id, action, action_query_id, state
FROM snowflake.account_usage.alert_history
WHERE COMPLETED_TIME > DATEADD(hours, -1, CURRENT_TIMESTAMP());