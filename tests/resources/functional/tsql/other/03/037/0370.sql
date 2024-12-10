-- tsql sql:
WITH temp_result AS (SELECT 'SID5678' AS session_id)
SELECT 'KILL ' + session_id AS kill_command
FROM temp_result;
