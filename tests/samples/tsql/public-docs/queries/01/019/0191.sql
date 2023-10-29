-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT fis.SalesOrderNumber,
    dp.ProductKey,
    dp.EnglishProductName
FROM FactInternetSales AS fis
INNER JOIN DimProduct AS dp
    ON dp.ProductKey = fis.ProductKey
WHERE fis.SalesOrderNumber > 'SO50000'
ORDER BY fis.SalesOrderNumber;