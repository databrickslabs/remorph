-- tsql sql:
WITH customer_orders AS (
    SELECT orderkey, orderdate, totalprice, orderstatus
    FROM (
        VALUES (1, '2020-01-01', 100.0, 'Shipped'),
               (2, '2020-01-02', 200.0, 'Pending'),
               (3, '2020-01-03', 300.0, 'Delivered')
    ) AS orders (orderkey, orderdate, totalprice, orderstatus)
),
average_price AS (
    SELECT AVG(totalprice) AS avg_price
    FROM customer_orders
)
SELECT 'Anomaly detected' AS message, orderkey, orderdate, totalprice, orderstatus
FROM customer_orders
CROSS JOIN average_price
WHERE totalprice > avg_price * 1.5
