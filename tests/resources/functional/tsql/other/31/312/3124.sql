--Query type: DCL
WITH cte_filegroup AS (SELECT 2 AS filegroup_id, 'SECONDARY' AS filegroup_name), cte_dbcc AS (SELECT 'CHECKFILEGROUP' AS dbcc_command, 2 AS filegroup_id, 'NOINDEX' AS option_name) SELECT T1.filegroup_name, T2.dbcc_command, T2.option_name FROM cte_filegroup AS T1 INNER JOIN cte_dbcc AS T2 ON T1.filegroup_id = T2.filegroup_id
