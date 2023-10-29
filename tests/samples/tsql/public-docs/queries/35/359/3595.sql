-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver16

USE ssawPDW;
  
SELECT DISTINCT COUNT(ProductKey) OVER(PARTITION BY SalesOrderNumber) AS ProductCount
    , SalesOrderNumber
FROM dbo.FactInternetSales
WHERE SalesOrderNumber IN (N'SO53115',N'SO55981');