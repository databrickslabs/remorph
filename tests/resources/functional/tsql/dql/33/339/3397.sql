-- tsql sql:
WITH temp_result AS (
    SELECT 'customer' AS name, 1 AS object_id, 1 AS schema_id, 'table' AS type_desc
    UNION ALL
    SELECT 'orders', 2, 1, 'table'
    UNION ALL
    SELECT 'lineitem', 3, 1, 'table'
)
SELECT name, object_id, schema_id, type_desc
FROM temp_result
WHERE OBJECTPROPERTYEX(object_id, N'TableHasForeignKey') = 1
ORDER BY name;
