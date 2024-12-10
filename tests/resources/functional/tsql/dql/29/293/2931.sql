-- tsql sql:
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 1 AS CustomerID
),
EmailCTE AS (
    SELECT 'john.doe@example.com' AS EmailAddress, 1 AS CustomerID
)
SELECT c.FirstName + ' ' + c.LastName + CHAR(13) + e.EmailAddress
FROM CustomerCTE c
INNER JOIN EmailCTE e ON c.CustomerID = e.CustomerID AND c.CustomerID = 1
