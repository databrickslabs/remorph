--Query type: DCL
WITH customer AS (
    SELECT 1 AS custkey, 'Customer 1' AS name, 1 AS nationkey
    UNION ALL
    SELECT 2, 'Customer 2', 2
),
orders AS (
    SELECT 1 AS orderkey, 1 AS custkey, 1000.0 AS totalprice
    UNION ALL
    SELECT 2, 1, 2000.0
    UNION ALL
    SELECT 3, 2, 500.0
),
filtered_orders AS (
    SELECT orderkey
    FROM orders
    WHERE totalprice > 500
)
SELECT c.custkey, c.name, SUM(o.totalprice) AS total_revenue
FROM customer c
JOIN orders o
    ON c.custkey = o.custkey
WHERE c.nationkey = 1
    AND o.orderkey IN (
        SELECT orderkey
        FROM filtered_orders
    )
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 1000000
ORDER BY total_revenue DESC