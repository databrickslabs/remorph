--Query type: DQL
WITH cte AS (
    SELECT 'customer' AS table_name, 'c_name' AS column_name, 'SELECT' AS privilege_type
    UNION ALL
    SELECT 'orders', 'o_orderkey', 'INSERT'
)
SELECT table_name, column_name, HAS_PERMS_BY_NAME(table_name, 'OBJECT', privilege_type, column_name, 'COLUMN') AS can_select
FROM cte
WHERE object_id(table_name) = object_id('customer');