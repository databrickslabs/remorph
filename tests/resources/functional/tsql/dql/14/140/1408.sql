--Query type: DQL
WITH cte AS (SELECT 'dbcc_checkdb' AS dbcc_function)
SELECT 'DBCC ' + dbcc_function
FROM cte;