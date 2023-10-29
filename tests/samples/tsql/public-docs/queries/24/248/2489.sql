-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver16

SELECT COUNT(*), AVG(Bonus)
FROM Sales.SalesPerson
WHERE SalesQuota > 25000;
GO