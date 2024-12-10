-- tsql sql:
WITH EmployeeCTE AS (
    SELECT 'John' AS FName, 'Doe' AS LName, 1 AS SalesTerritoryKey
    UNION ALL
    SELECT 'Jane', 'Doe', 2
),
GeographyCTE AS (
    SELECT 'Australia' AS Country, 1 AS SalesTerritoryKey
    UNION ALL
    SELECT 'USA', 2
)
SELECT DISTINCT LEN(FName) AS FNameLength, FName, LName
FROM EmployeeCTE AS e
INNER JOIN GeographyCTE AS g ON e.SalesTerritoryKey = g.SalesTerritoryKey
WHERE Country = 'Australia';
