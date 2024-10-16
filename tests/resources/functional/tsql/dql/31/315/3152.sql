--Query type: DQL
WITH Sales AS (
    SELECT 10 AS OrderQty, 100.0 AS UnitPrice
    UNION ALL
    SELECT 20, 200.0
    UNION ALL
    SELECT 30, 300.0
)
SELECT AVG(OrderQty) AS [Average Quantity],
       NonDiscountSales = (OrderQty * UnitPrice)
FROM Sales
GROUP BY (OrderQty * UnitPrice)
ORDER BY (OrderQty * UnitPrice) DESC;