--Query type: DQL
WITH temp_result AS (
    SELECT 'TABLE' AS resource_type, 1 AS resource_database_id, 'IX' AS request_mode, 'INSERT' AS request_type, 'GRANT' AS request_status, 1 AS request_session_id
    UNION ALL
    SELECT 'INDEX', 2, 'S', 'SELECT', 'CONVERT', 2
)
SELECT resource_type, resource_database_id, request_mode, request_type, request_status, request_session_id
FROM temp_result
WHERE resource_database_id = DB_ID(N'customer');
