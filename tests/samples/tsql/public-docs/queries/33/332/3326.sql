-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT AVG(UnitPrice) AS [Average Price]  
FROM Sales.SalesOrderDetail;