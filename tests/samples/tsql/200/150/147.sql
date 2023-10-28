-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    dst.SalesTerritoryRegion,
    fis.SalesOrderNumber
FROM FactInternetSales AS fis
RIGHT OUTER JOIN DimSalesTerritory AS dst
    ON fis.SalesTerritoryKey = dst.SalesTerritoryKey
ORDER BY fis.SalesOrderNumber;