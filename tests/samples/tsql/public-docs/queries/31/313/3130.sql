-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freesessioncache-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC FREESESSIONCACHE WITH NO_INFOMSGS;
GO