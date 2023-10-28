-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    fis.SalesOrderNumber
FROM DimSalesTerritory AS dst
CROSS JOIN FactInternetSales AS fis
ORDER BY fis.SalesOrderNumber;