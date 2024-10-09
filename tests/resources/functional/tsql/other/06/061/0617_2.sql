--Query type: DDL
WITH temp_result AS (
    SELECT 'mydb' AS db_name
)
SELECT 'DROP DATABASE IF EXISTS ' + db_name + ' RESTRICT;' AS query
FROM temp_result;