-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-help-transact-sql?view=sql-server-ver16

DECLARE @dbcc_stmt sysname;
SET @dbcc_stmt = 'CHECKDB';
DBCC HELP (@dbcc_stmt);
GO