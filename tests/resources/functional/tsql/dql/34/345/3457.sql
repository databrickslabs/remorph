-- tsql sql:
WITH SalesPerson AS (
    SELECT 1 AS SalesPersonID, 1000 AS SalesYTD, 1 AS TerritoryID
),
Person AS (
    SELECT 1 AS PersonID, 'John' AS FirstName, 'Doe' AS LastName, 1 AS BusinessEntityID
),
Address AS (
    SELECT 1 AS AddressID, '123 Main St' AS PostalCode
)
SELECT
    p.FirstName,
    p.LastName,
    NTILE(4) OVER (ORDER BY sp.SalesYTD DESC) AS Quartile,
    CONVERT(NVARCHAR(20), sp.SalesYTD, 1) AS SalesYTD,
    a.PostalCode
FROM
    SalesPerson sp
    INNER JOIN Person p ON sp.SalesPersonID = p.PersonID
    INNER JOIN Address a ON a.AddressID = p.BusinessEntityID
WHERE
    sp.TerritoryID IS NOT NULL
    AND sp.SalesYTD <> 0
