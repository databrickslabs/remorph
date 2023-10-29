-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver16

USE ssawPDW;
  
SELECT COUNT(EmployeeKey) AS TotalCount, AVG(SalesAmountQuota) AS [Average Sales Quota]
FROM dbo.FactSalesQuota
WHERE SalesAmountQuota > 500000 AND CalendarYear = 2001;