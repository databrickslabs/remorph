--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'Smith' AS LastName, 'John' AS FirstName, 1 AS CustomerID
),
OrderCTE AS (
    SELECT 1 AS OrderID, 1 AS CustomerID, 'Sales Person' AS JobTitle
)
SELECT c.LastName, c.FirstName, o.JobTitle
INTO #CustomerOne
FROM CustomerCTE c
INNER JOIN OrderCTE o ON o.CustomerID = c.CustomerID
WHERE c.LastName = 'Smith';
