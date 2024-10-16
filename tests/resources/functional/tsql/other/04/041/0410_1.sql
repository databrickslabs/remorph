--Query type: DDL
DECLARE @sql nvarchar(max) = '';

WITH files_to_add AS (
    SELECT 'file1' AS filename, 'd:\data\file1' AS filepath, 100 AS size
    UNION ALL
    SELECT 'file2', 'd:\data\file2', 200
    UNION ALL
    SELECT 'file3', 'd:\data\file3', 300
)

SELECT @sql += '
ALTER DATABASE xtp_db
ADD FILE
(
    NAME=''' + filename + ''',
    FILENAME=''' + filepath + '''
)
TO FILEGROUP xtp_fg;
'
FROM files_to_add;

PRINT @sql; -- EXEC sp_executesql @sql; -- Uncomment to execute the generated SQL