-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT dp.ProductKey,
    fis.SalesOrderNumber,
    fis.TotalProductCost
FROM DimProduct AS dp
INNER REDISTRIBUTE JOIN FactInternetSales AS fis
    ON dp.ProductKey = fis.ProductKey;