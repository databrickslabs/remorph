-- tsql sql:
WITH temp_result AS (SELECT 'customer' AS table_name, 'OBJECT' AS securable_class, 'INSERT' AS permission_name)
SELECT HAS_PERMS_BY_NAME(table_name, securable_class, permission_name)
FROM temp_result;
