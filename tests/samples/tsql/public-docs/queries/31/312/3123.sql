-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkconstraints-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC CHECKCONSTRAINTS ('Production.CK_ProductCostHistory_EndDate');
GO