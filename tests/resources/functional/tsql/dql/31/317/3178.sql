--Query type: DQL
WITH OrderDetails AS (
    SELECT 1 AS OrderID, 10.0 AS LineTotal
    UNION ALL
    SELECT 2, 20.0
    UNION ALL
    SELECT 3, 30.0
)
SELECT OrderID, SUM(LineTotal) AS SubTotal
FROM OrderDetails
GROUP BY OrderID
ORDER BY OrderID
