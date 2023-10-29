-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-cleantable-transact-sql?view=sql-server-ver16

DBCC CLEANTABLE (AdventureWorks2022, 'Production.Document', 1000)
WITH NO_INFOMSGS;
GO