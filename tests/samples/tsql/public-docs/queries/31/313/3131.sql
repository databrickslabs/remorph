-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-showcontig-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC SHOWCONTIG ('HumanResources.Employee');
GO