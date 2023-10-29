-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dbreindex-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC DBREINDEX ('HumanResources.Employee', ' ', 70);
GO