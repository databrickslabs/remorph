--Query type: DQL
WITH temp_result AS (
    SELECT 'customer' AS table_name, 1 AS schema_id
    UNION ALL
    SELECT 'orders', 1
)
SELECT HAS_PERMS_BY_NAME(QUOTENAME(SCHEMA_NAME(schema_id)) + '.' + QUOTENAME(table_name), 'OBJECT', 'SELECT') AS have_select, *
FROM temp_result
