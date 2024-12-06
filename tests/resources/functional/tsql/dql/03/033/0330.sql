-- tsql sql:
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 1 AS CustomerID
    UNION ALL
    SELECT 'Jane', 'Doe', 2
),
OrdersCTE AS (
    SELECT 1 AS OrderID, 1 AS CustomerID, 'Sales Representative' AS JobTitle
    UNION ALL
    SELECT 2, 2, 'Sales Manager'
)
SELECT c.FirstName, c.LastName, o.JobTitle
FROM CustomerCTE c
JOIN OrdersCTE o ON c.CustomerID = o.CustomerID
WHERE o.JobTitle IN ('Sales Representative', 'Sales Manager', 'Sales Engineer');
