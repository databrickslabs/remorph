-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql?view=sql-server-ver16

-- Check the current database.
DBCC CHECKDB;
GO
-- Check the AdventureWorks2022 database without nonclustered indexes.
DBCC CHECKDB (AdventureWorks2022, NOINDEX);
GO