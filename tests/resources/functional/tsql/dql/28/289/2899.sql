-- tsql sql:
WITH temp_result AS (
    SELECT 'customer[_]segment' AS name, 'V' AS type, 'public' AS schema_name
    UNION ALL
    SELECT 'supplier[_]nation', 'V', 'public'
    UNION ALL
    SELECT 'orders[_]status', 'V', 'public'
)
SELECT name
FROM temp_result
WHERE (
    name LIKE 'customer[_]%' OR name LIKE 'supplier[_]%'
)
AND name LIKE '%[_]status%'
AND type = 'V'
AND schema_name = 'public'
ORDER BY name;
