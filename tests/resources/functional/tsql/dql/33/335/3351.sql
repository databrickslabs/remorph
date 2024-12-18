-- tsql sql:
WITH temp_result AS (SELECT 'TPC-H' AS database_name)
SELECT GETANSINULL(database_name)
FROM temp_result
