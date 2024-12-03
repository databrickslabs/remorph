--Query type: DDL
WITH customer AS (
    SELECT 1 AS custkey, 'Customer1' AS name, 1 AS nationkey
    UNION ALL
    SELECT 2, 'Customer2', 2
),
orders AS (
    SELECT 1 AS orderkey, 1 AS custkey, 1000.0 AS totalprice
    UNION ALL
    SELECT 2, 1, 2000.0
    UNION ALL
    SELECT 3, 2, 500.0
)
SELECT c.custkey, c.name, SUM(o.totalprice) AS total
FROM customer c
JOIN orders o ON c.custkey = o.custkey
WHERE c.nationkey = 1
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 3000
ORDER BY total DESC;
