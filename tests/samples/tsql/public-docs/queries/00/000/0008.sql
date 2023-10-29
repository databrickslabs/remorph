-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkcatalog-transact-sql?view=sql-server-ver16

-- Check the current database.
DBCC CHECKCATALOG;
GO
-- Check the AdventureWorks database.
DBCC CHECKCATALOG (AdventureWorks2022);
GO