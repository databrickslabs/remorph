--Query type: DDL
WITH temp_result AS (SELECT 'MyNewOptionsTest' AS database_name, 'Latin1_General_CI_AS' AS collation_name)
SELECT 'CREATE DATABASE ' + database_name + ' COLLATE ' + collation_name + ' WITH TRUSTWORTHY ON, DB_CHAINING ON;' AS query
FROM temp_result