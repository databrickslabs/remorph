-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

SELECT CAST(ROUND(SalesYTD / CommissionPCT, 0) AS INT) AS Computed
FROM Sales.SalesPerson
WHERE CommissionPCT != 0;
GO