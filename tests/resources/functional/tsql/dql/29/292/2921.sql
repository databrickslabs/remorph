-- tsql sql:
WITH database_info AS ( SELECT 'database_name' AS name, 1 AS is_result_set_caching_on UNION ALL SELECT 'database_name2', 0 ) SELECT name, is_result_set_caching_on FROM database_info WHERE name = 'database_name'
