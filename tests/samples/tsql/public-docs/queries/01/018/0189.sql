-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT dst.SalesTerritoryKey,
    fis.SalesOrderNumber
FROM DimSalesTerritory AS dst
CROSS JOIN FactInternetSales AS fis
ORDER BY fis.SalesOrderNumber;