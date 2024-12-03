--Query type: DQL
WITH cte AS (SELECT 'customer' AS table_name, 'OBJECT' AS securable_class, 'INSERT' AS permission_name)
SELECT HAS_PERMS_BY_NAME(cte.table_name, cte.securable_class, cte.permission_name)
FROM cte
