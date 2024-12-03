--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Doe' AS LastName, 1 AS CustomerID
    UNION ALL
    SELECT 'Jane' AS FirstName, 'Doe' AS LastName, 2 AS CustomerID
),
OrdersCTE AS (
    SELECT 1 AS OrderID, 1 AS CustomerID, 'Sales Engineer' AS JobTitle
    UNION ALL
    SELECT 2 AS OrderID, 2 AS CustomerID, 'Marketing Assistant' AS JobTitle
    UNION ALL
    SELECT 3 AS OrderID, 1 AS CustomerID, 'Tool Designer' AS JobTitle
)
SELECT c.FirstName, c.LastName, o.JobTitle
FROM CustomerCTE c
JOIN OrdersCTE o ON c.CustomerID = o.CustomerID
WHERE o.JobTitle = 'Sales Engineer' OR o.JobTitle = 'Marketing Assistant' OR o.JobTitle = 'Tool Designer';
