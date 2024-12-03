--Query type: DQL
WITH SalesPersonCTE AS (
    SELECT 1 AS CustomerID, 10 AS TerritoryID, 1000.00 AS SalesYTD, '2020-01-01' AS ModifiedDate
    UNION ALL
    SELECT 2 AS CustomerID, 20 AS TerritoryID, 2000.00 AS SalesYTD, '2020-02-01' AS ModifiedDate
    UNION ALL
    SELECT 3 AS CustomerID, 30 AS TerritoryID, 3000.00 AS SalesYTD, '2020-03-01' AS ModifiedDate
)
SELECT CustomerID, TerritoryID, CONVERT(VARCHAR(20), SalesYTD, 1) AS SalesYTD, DATEPART(yy, ModifiedDate) AS SalesYear, CONVERT(VARCHAR(20), SUM(SalesYTD) OVER (PARTITION BY TerritoryID ORDER BY DATEPART(yy, ModifiedDate) ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING), 1) AS CumulativeTotal
FROM SalesPersonCTE
WHERE TerritoryID IS NULL OR TerritoryID < 5;
