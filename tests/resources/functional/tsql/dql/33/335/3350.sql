--Query type: DQL
WITH SalesPersonCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 'North' AS TerritoryName, 1000.50 AS SalesYTD
    UNION ALL
    SELECT 'Jane', 'Doe', 'South', 2000.25
    UNION ALL
    SELECT 'Bob', 'Smith', 'East', 3000.00
)
SELECT FirstName, LastName, TerritoryName, ROUND(SalesYTD, 2, 1) AS SalesYTD, ROW_NUMBER() OVER (PARTITION BY TerritoryName ORDER BY SalesYTD DESC) AS Row
FROM SalesPersonCTE
WHERE TerritoryName IS NOT NULL AND SalesYTD <> 0
ORDER BY TerritoryName;
