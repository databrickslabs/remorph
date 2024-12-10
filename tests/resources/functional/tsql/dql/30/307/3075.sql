-- tsql sql:
WITH CustomerInfo AS (
    SELECT 1 AS CustomerID, 'John' AS FirstName, 'Doe' AS LastName, 'Customer' AS ContactType
    UNION ALL
    SELECT 2, 'Jane', 'Doe', 'Supplier'
)
SELECT dbo.GetContactInformation(CustomerID), FirstName, LastName, ContactType
FROM CustomerInfo
WHERE CustomerID = 1
