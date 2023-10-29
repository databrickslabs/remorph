-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    dst.SalesTerritoryRegion,
    fis.SalesOrderNumber
FROM DimSalesTerritory AS dst
LEFT OUTER JOIN FactInternetSales AS fis
    ON dst.SalesTerritoryKey = fis.SalesTerritoryKey
ORDER BY fis.SalesOrderNumber;