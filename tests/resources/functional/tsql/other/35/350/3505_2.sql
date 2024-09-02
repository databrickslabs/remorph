--Query type: DDL
WITH DBInfo AS (
    SELECT 'BlobStore2' AS DBName, 'C:\BlobStore\FS4' AS FileName, '200MB' AS MaxSize
)
SELECT 'ALTER DATABASE [' + DBName + '] ADD FILE ( NAME = N''FS4'', FILENAME = N''' + FileName + ''', MAXSIZE = ' + MaxSize + ' ) TO FILEGROUP [FS];' AS SQLStatement
FROM DBInfo