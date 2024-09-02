--Query type: DQL
DECLARE @NTILE_Var INT = 4;

WITH SalesPerson AS (
    SELECT 1 AS BusinessEntityID, 1000 AS SalesYTD, 1 AS TerritoryID
),
Person AS (
    SELECT 1 AS BusinessEntityID, 'John' AS FirstName, 'Doe' AS LastName
),
Address AS (
    SELECT 1 AS AddressID, '123 Main St' AS PostalCode
)

SELECT p.FirstName, p.LastName, NTILE(@NTILE_Var) OVER (PARTITION BY a.PostalCode ORDER BY s.SalesYTD DESC) AS Quartile,
       CONVERT(NVARCHAR(20), s.SalesYTD, 1) AS SalesYTD, a.PostalCode
FROM SalesPerson AS s
INNER JOIN Person AS p ON s.BusinessEntityID = p.BusinessEntityID
INNER JOIN Address AS a ON a.AddressID = p.BusinessEntityID
WHERE s.TerritoryID IS NOT NULL AND s.SalesYTD <> 0;