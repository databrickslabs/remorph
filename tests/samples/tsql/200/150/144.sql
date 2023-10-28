-- Uses AdventureWorks
  
SELECT fis.SalesOrderNumber,
    dp.ProductKey,
    dp.EnglishProductName
FROM FactInternetSales AS fis
LEFT OUTER JOIN DimProduct AS dp
    ON dp.ProductKey = fis.ProductKey;