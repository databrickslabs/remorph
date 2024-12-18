-- tsql sql:
WITH temp_result AS (
    SELECT 3 AS db_id
)
SELECT DB_NAME(db_id) AS [Database Name]
FROM temp_result;
