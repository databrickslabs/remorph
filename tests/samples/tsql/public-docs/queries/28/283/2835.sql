-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT TerritoryID,
    Name
FROM Sales.SalesTerritory
ORDER BY TerritoryID;