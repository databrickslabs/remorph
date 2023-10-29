-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/stdev-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT STDEV(DISTINCT SalesAmountQuota)AS Distinct_Values, STDEV(SalesAmountQuota) AS All_Values  
FROM dbo.FactSalesQuota;