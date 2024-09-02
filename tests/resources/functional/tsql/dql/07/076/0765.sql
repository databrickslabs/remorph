--Query type: DQL
WITH temp_result AS (
    SELECT 'MYDB.MYSCHEMA.' AS name_prefix, 1 AS error_only
),
refresh_history AS (
    SELECT name, state, state_code, state_message, query_id, data_timestamp, refresh_start_time, refresh_end_time
    FROM sys.dm_pdw_exec_requests
    WHERE database_name = (SELECT name_prefix FROM temp_result)
    AND error_only = (SELECT error_only FROM temp_result)
)
SELECT *
FROM refresh_history
ORDER BY name, data_timestamp;