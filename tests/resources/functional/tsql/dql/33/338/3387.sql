--Query type: DQL
WITH SalesPersonCTE AS (
    SELECT 'Northwest' AS TerritoryName, 1 AS BusinessEntityID, 1000.0 AS SalesYTD
    UNION ALL
    SELECT 'Canada', 2, 2000.0
    UNION ALL
    SELECT 'Northwest', 3, 3000.0
    UNION ALL
    SELECT 'Canada', 4, 4000.0
)
SELECT TerritoryName, BusinessEntityID, SalesYTD, LEAD(SalesYTD, 1, 0) OVER (PARTITION BY TerritoryName ORDER BY SalesYTD DESC) AS NextRepSales
FROM SalesPersonCTE
WHERE TerritoryName IN ('Northwest', 'Canada')
ORDER BY TerritoryName;
