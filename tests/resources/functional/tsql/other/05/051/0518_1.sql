--Query type: DML
SELECT *
INTO #NewOrders
FROM (
    VALUES
        (1, '2020-01-01', 100.00),
        (2, '2020-01-15', 200.00),
        (3, '2020-02-01', 50.00)
) AS Orders (OrderKey, OrderDate, TotalPrice);

WITH OrderCTE AS (
    SELECT OrderKey, OrderDate, TotalPrice
    FROM #NewOrders
)
SELECT *
FROM OrderCTE
WHERE TotalPrice > 50 AND TotalPrice < 200;
-- REMORPH CLEANUP: DROP TABLE #NewOrders;