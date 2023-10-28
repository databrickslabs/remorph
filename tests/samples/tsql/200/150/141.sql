-- Uses AdventureWorks
  
SELECT fis.SalesOrderNumber,
    dp.ProductKey,
    dp.EnglishProductName
FROM FactInternetSales AS fis
INNER JOIN DimProduct AS dp
    ON dp.ProductKey = fis.ProductKey;