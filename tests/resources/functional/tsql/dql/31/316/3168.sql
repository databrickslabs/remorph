--Query type: DQL
WITH SalesOrderDetail AS (
    SELECT ProductKey, UnitPrice, OrderQuantity
    FROM (
        VALUES (1, 10.0, 5),
               (2, 20.0, 15),
               (3, 30.0, 20)
    ) AS SalesOrderDetail (ProductKey, UnitPrice, OrderQuantity)
)
SELECT ProductKey, AVG(UnitPrice) AS AveragePrice
FROM SalesOrderDetail
WHERE OrderQuantity > 10
GROUP BY ProductKey
ORDER BY AVG(UnitPrice);