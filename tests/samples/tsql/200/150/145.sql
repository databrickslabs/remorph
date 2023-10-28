-- Uses AdventureWorks
  
SELECT fis.SalesOrderNumber,
    dp.ProductKey,
    dp.EnglishProductName
FROM DimProduct AS dp
RIGHT OUTER JOIN FactInternetSales AS fis
    ON dp.ProductKey = fis.ProductKey;