--Query type: DDL
DECLARE @filename nvarchar(50), @filepath nvarchar(255), @sql nvarchar(max);

WITH temp_data AS (
    SELECT 'tempdev' AS filename, 'E:\SQLData\tempdb.mdf' AS filepath
)

SELECT TOP 1 @filename = filename, @filepath = filepath
FROM temp_data;

SET @sql = N'ALTER DATABASE tempdb MODIFY FILE (NAME = ''' + @filename + ''', FILENAME = ''' + @filepath + ''');';

EXEC sp_executesql @sql;

SELECT * FROM tempdb.sys.database_files;
-- REMORPH CLEANUP: No tables were created, so no DROP statements are needed.