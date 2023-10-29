-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    dst.SalesTerritoryRegion,
    fis.SalesOrderNumber
FROM FactInternetSales AS fis
RIGHT OUTER JOIN DimSalesTerritory AS dst
    ON fis.SalesTerritoryKey = dst.SalesTerritoryKey
ORDER BY fis.SalesOrderNumber;