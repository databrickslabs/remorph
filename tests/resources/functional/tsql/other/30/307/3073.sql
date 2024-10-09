--Query type: DCL
WITH customer AS (
    SELECT 1 AS custkey, 'Customer 1' AS name, 1 AS nationkey
    UNION ALL
    SELECT 2, 'Customer 2', 2
),
orders AS (
    SELECT 1 AS orderkey, 1 AS custkey, '1995-01-01' AS orderdate, 1000.0 AS totalprice
    UNION ALL
    SELECT 2, 1, '1995-01-02', 2000.0
    UNION ALL
    SELECT 3, 2, '1995-01-03', 3000.0
)
SELECT TOP 10
    c.custkey,
    c.name,
    SUM(o.totalprice) AS total_revenue
FROM customer c
JOIN orders o
    ON c.custkey = o.custkey
WHERE c.nationkey = 1 AND o.orderdate >= '1995-01-01'
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 100000
ORDER BY total_revenue DESC;