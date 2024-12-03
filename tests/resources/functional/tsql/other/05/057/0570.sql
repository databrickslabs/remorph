--Query type: DDL
WITH temp AS (SELECT 'dw1' AS database_name, 10240 AS max_size)
SELECT 'ALTER DATABASE ' + database_name + ' MODIFY ( MAXSIZE=' + CONVERT(VARCHAR, max_size) + ' GB );' AS query
FROM temp
