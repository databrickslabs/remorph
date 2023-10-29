-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/min-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT DISTINCT MIN(UnitPrice)  
FROM dbo.FactResellerSales   
WHERE SalesOrderNumber IN (N'SO43659', N'SO43660', N'SO43664');