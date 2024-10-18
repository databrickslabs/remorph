--Query type: DDL
WITH orders AS (
    SELECT '1-URGENT' AS orderpriority, 10.0 AS extendedprice, '1993-07-01' AS orderdate, 1 AS shippriority, 0 AS discount
    UNION ALL
    SELECT '2-HIGH', 20.0, '1993-07-02', 2, 0
    UNION ALL
    SELECT '3-MEDIUM', 30.0, '1993-07-03', 3, 0
)
SELECT TOP 10
    CASE
        WHEN orderpriority = '1-URGENT' OR orderpriority = '2-HIGH' THEN 'High'
        ELSE 'Low'
    END AS order_priority,
    SUM(extendedprice * (1 - discount)) AS revenue,
    orderdate,
    shippriority
FROM orders
WHERE orderdate >= '1993-07-01' AND orderdate < '1993-10-01'
GROUP BY
    CASE
        WHEN orderpriority = '1-URGENT' OR orderpriority = '2-HIGH' THEN 'High'
        ELSE 'Low'
    END,
    orderdate,
    shippriority
ORDER BY revenue DESC, orderdate