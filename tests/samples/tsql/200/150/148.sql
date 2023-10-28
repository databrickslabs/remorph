-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    dst.SalesTerritoryRegion,
    fis.SalesOrderNumber
FROM DimSalesTerritory AS dst
FULL JOIN FactInternetSales AS fis
    ON dst.SalesTerritoryKey = fis.SalesTerritoryKey
ORDER BY fis.SalesOrderNumber;