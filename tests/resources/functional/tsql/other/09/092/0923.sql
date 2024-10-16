--Query type: DDL
WITH orders AS (
    SELECT '1-URGENT' AS order_priority, 100.0 AS extended_price, '1993-01-01' AS order_date, 1 AS ship_priority, 0 AS discount
    UNION ALL
    SELECT '2-HIGH', 200.0, '1993-01-02', 2, 0
    UNION ALL
    SELECT '3-MEDIUM', 300.0, '1993-01-03', 3, 0
)
SELECT
    CASE
        WHEN SUM(CASE WHEN order_priority = '1-URGENT' OR order_priority = '2-HIGH' THEN 1 ELSE 0 END) > 0 THEN 'High'
        ELSE 'Low'
    END AS order_priority,
    SUM(extended_price * (1 - discount)) AS revenue,
    order_date,
    ship_priority
FROM orders
WHERE order_date >= '1993-01-01' AND order_date < '1994-01-01'
GROUP BY order_date, ship_priority
ORDER BY order_date, ship_priority
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY;