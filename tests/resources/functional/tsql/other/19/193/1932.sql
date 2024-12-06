-- tsql sql:
WITH temp_result AS (
    SELECT 'customer' AS type, 1 AS id, COALESCE('John', 'Unknown') AS name
    UNION ALL
    SELECT 'supplier', 2, COALESCE('Jane', 'Unknown')
)
SELECT SUSER_NAME() AS [current_user], type, id, name
FROM temp_result
