-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql?view=sql-server-ver16

DBCC CLONEDATABASE (AdventureWorks2022, AdventureWorks_Clone) WITH NO_STATISTICS, NO_QUERYSTORE;
GO