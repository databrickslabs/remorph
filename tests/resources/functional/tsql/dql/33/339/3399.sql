--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 1 AS CustomerID
),
AddressCTE AS (
    SELECT '123 Main St' AS StreetAddress, 'Anytown' AS City, '12345' AS PostalCode, 1 AS AddressID
),
SalesCTE AS (
    SELECT 1 AS SalesID, 1 AS CustomerID, 100.00 AS SalesAmount, 1 AS TerritoryID
)
SELECT
    c.FirstName,
    c.LastName,
    DATEDIFF(day, ROW_NUMBER() OVER (ORDER BY a.PostalCode), SYSDATETIME()) AS 'Row Number'
FROM
    SalesCTE s
    INNER JOIN CustomerCTE c ON s.CustomerID = c.CustomerID
    INNER JOIN AddressCTE a ON a.AddressID = c.CustomerID
WHERE
    s.TerritoryID IS NOT NULL
    AND s.SalesAmount <> 0
