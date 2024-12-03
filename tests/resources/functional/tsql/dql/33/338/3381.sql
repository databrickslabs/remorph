--Query type: DQL
SELECT s.name AS TABLE_SCHEMA, t.name AS TABLE_NAME, t.identity_increment_value AS IDENT_INCR
FROM (
    SELECT 1 AS schema_id, 'customer' AS name, 1 AS is_identity, 1 AS identity_increment_value
    UNION ALL
    SELECT 1, 'orders', 1, 1
    UNION ALL
    SELECT 1, 'lineitem', 0, NULL
) t
INNER JOIN (
    SELECT 1 AS schema_id, 'dbo' AS name
) s
ON t.schema_id = s.schema_id
WHERE t.name IN ('customer', 'orders', 'lineitem')
AND t.is_identity = 1;
