-- tsql sql:
WITH temp_result AS (SELECT 'Customer' AS table_name)
SELECT IDENT_INCR(table_name) AS Identity_Increment
FROM temp_result;
