-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkfilegroup-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC CHECKFILEGROUP (1, NOINDEX);
GO