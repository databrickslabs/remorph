-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkfile-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SELECT file_id, name
FROM sys.database_files;
GO
DBCC SHRINKFILE (1, TRUNCATEONLY);