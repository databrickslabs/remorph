-- tsql sql:
WITH SalesPersonCTE AS (
    SELECT 1 AS BusinessEntityID, 1000 AS SalesYTD, 1 AS TerritoryID
    UNION ALL
    SELECT 2, 2000, 2
    UNION ALL
    SELECT 3, 3000, 3
),
PersonCTE AS (
    SELECT 1 AS BusinessEntityID, 'John' AS FirstName, 'Doe' AS LastName
    UNION ALL
    SELECT 2, 'Jane', 'Doe'
    UNION ALL
    SELECT 3, 'Bob', 'Smith'
),
AddressCTE AS (
    SELECT 1 AS AddressID, '123 Main St' AS PostalCode
    UNION ALL
    SELECT 2, '456 Elm St'
    UNION ALL
    SELECT 3, '789 Oak St'
)
SELECT
    p.FirstName,
    p.LastName,
    ROW_NUMBER() OVER (ORDER BY a.PostalCode) AS [Row Number],
    RANK() OVER (ORDER BY a.PostalCode) AS Rank,
    DENSE_RANK() OVER (ORDER BY a.PostalCode) AS [Dense Rank],
    NTILE(4) OVER (ORDER BY a.PostalCode) AS Quartile,
    s.SalesYTD,
    a.PostalCode
FROM
    SalesPersonCTE AS s
    INNER JOIN PersonCTE AS p ON s.BusinessEntityID = p.BusinessEntityID
    INNER JOIN AddressCTE AS a ON a.AddressID = p.BusinessEntityID
WHERE
    TerritoryID IS NOT NULL
    AND SalesYTD <> 0;
