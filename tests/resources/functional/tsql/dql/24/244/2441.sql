-- tsql sql:
WITH SalesPersonCTE AS (
    SELECT 1 AS BusinessEntityID, 1 AS TerritoryID, '2020-01-01' AS ModifiedDate, 1000.00 AS SalesYTD
    UNION ALL
    SELECT 2, 2, '2020-02-01', 2000.00
    UNION ALL
    SELECT 3, 3, '2020-03-01', 3000.00
    UNION ALL
    SELECT 4, 4, '2020-04-01', 4000.00
    UNION ALL
    SELECT 5, 5, '2020-05-01', 5000.00
)
SELECT BusinessEntityID, TerritoryID, DATEPART(yy, ModifiedDate) AS SalesYear, CONVERT(VARCHAR(20), SalesYTD, 1) AS SalesYTD, CONVERT(VARCHAR(20), AVG(SalesYTD) OVER (ORDER BY DATEPART(yy, ModifiedDate)), 1) AS MovingAvg, CONVERT(VARCHAR(20), SUM(SalesYTD) OVER (ORDER BY DATEPART(yy, ModifiedDate)), 1) AS CumulativeTotal
FROM SalesPersonCTE
WHERE TerritoryID IS NULL OR TerritoryID < 5
ORDER BY SalesYear;
