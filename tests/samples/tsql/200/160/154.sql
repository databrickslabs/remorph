-- Uses AdventureWorks
  
SELECT dp.ProductKey,
    fis.SalesOrderNumber,
    fis.TotalProductCost
FROM DimProduct AS dp
INNER REDISTRIBUTE JOIN FactInternetSales AS fis
    ON dp.ProductKey = fis.ProductKey;