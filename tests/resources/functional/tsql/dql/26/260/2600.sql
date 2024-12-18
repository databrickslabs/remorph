-- tsql sql:
WITH temp_result AS (SELECT 1 AS filegroup_id)
SELECT FILEGROUP_NAME(filegroup_id) AS [Filegroup Name]
FROM temp_result;
