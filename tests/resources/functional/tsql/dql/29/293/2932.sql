-- tsql sql:
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 1001 AS CustomerID
),
AddressCTE AS (
    SELECT 1001 AS CustomerID, '123 Main St' AS StreetAddress, 'Anytown' AS City, '12345' AS PostalCode
),
OrderCTE AS (
    SELECT 1001 AS CustomerID, 10001 AS OrderID, 100.00 AS TotalDue
)
SELECT
    c.FirstName,
    c.LastName,
    DATEADD(day, ROW_NUMBER() OVER (ORDER BY a.PostalCode), SYSDATETIME()) AS 'Row Number'
FROM
    CustomerCTE c
    INNER JOIN AddressCTE a ON c.CustomerID = a.CustomerID
    INNER JOIN OrderCTE o ON c.CustomerID = o.CustomerID
WHERE
    o.TotalDue IS NOT NULL
    AND o.OrderID <> 0;
