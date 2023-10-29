-- see https://docs.snowflake.com/en/sql-reference/account-usage/snowpipe_streaming_client_history

SELECT COUNT(DISTINCT event_timestamp) AS client_seconds, date_trunc('hour',event_timestamp) AS event_hour, client_seconds*0.000002777777778 as credits, client_name, snowflake_provided_id
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPIPE_STREAMING_CLIENT_HISTORY
GROUP BY event_hour, client_name, snowflake_provided_id;