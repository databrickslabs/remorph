-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/varp-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT VARP(DISTINCT SalesAmountQuota)AS Distinct_Values, VARP(SalesAmountQuota) AS All_Values  
FROM dbo.FactSalesQuota;