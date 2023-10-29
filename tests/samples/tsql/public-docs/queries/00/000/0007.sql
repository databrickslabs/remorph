-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkalloc-transact-sql?view=sql-server-ver16

-- Check the current database.
DBCC CHECKALLOC;
GO
-- Check the AdventureWorks2022 database.
DBCC CHECKALLOC (AdventureWorks2022);
GO