-- tsql sql:
WITH SalesPerson AS (
    SELECT 1 AS BusinessEntityID, 10000 AS SalesYTD, 1 AS TerritoryID
),
Person AS (
    SELECT 1 AS BusinessEntityID, 'Doe' AS LastName
),
Address AS (
    SELECT 1 AS AddressID, '12345' AS PostalCode
)
SELECT
    ROW_NUMBER() OVER (PARTITION BY a.PostalCode ORDER BY s.SalesYTD DESC) AS [Row Number],
    p.LastName,
    s.SalesYTD,
    a.PostalCode
FROM
    SalesPerson AS s
    INNER JOIN Person AS p ON s.BusinessEntityID = p.BusinessEntityID
    INNER JOIN Address AS a ON a.AddressID = p.BusinessEntityID
WHERE
    s.TerritoryID IS NOT NULL AND s.SalesYTD <> 0
ORDER BY
    a.PostalCode
