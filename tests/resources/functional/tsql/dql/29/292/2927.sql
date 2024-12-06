-- tsql sql:
WITH temp_result AS ( SELECT 1 AS object_id, 'temp_name' AS name, 1 AS auto_drop UNION ALL SELECT 2, 'temp_name2', 0 ) SELECT object_id, name, auto_drop FROM temp_result;
