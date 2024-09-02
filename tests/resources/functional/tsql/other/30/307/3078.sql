--Query type: DDL
DECLARE @FileName nvarchar(50);
DECLARE @FileSize int;
DECLARE @sql nvarchar(max);

SET @FileName = 'test1dat3';
SET @FileSize = 200;

SET @sql = N'ALTER DATABASE AdventureWorks2022 MODIFY FILE ( NAME = ''' + @FileName + ''', SIZE = ' + CONVERT(nvarchar, @FileSize * 1024 * 1024) + ');'

EXEC sp_executesql @sql;

SELECT * FROM sys.master_files WHERE database_id = DB_ID('AdventureWorks2022');

-- REMORPH CLEANUP: No objects were created in this query, so no cleanup is necessary.