--Query type: DQL
WITH Products AS (
    SELECT 1 AS ProductID, 'Lock Washer 1' AS Name
    UNION ALL
    SELECT 2, 'Lock Washer 2'
    UNION ALL
    SELECT 3, 'Lock Washer 3'
)
SELECT ProductID, Name
FROM Products
WHERE Name LIKE 'Lock Washer%'
ORDER BY ProductID
