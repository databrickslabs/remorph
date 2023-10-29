-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/var-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT VAR(DISTINCT SalesAmountQuota)AS Distinct_Values, VAR(SalesAmountQuota) AS All_Values  
FROM dbo.FactSalesQuota;