--Query type: DDL
CREATE TABLE #customer (custkey INT, name VARCHAR(50), total DECIMAL(10, 2));
WITH customer AS (
    SELECT *
    FROM (
        VALUES (1, 'Customer1', 1),
               (2, 'Customer2', 2)
    ) AS c (custkey, name, nationkey)
),
orders AS (
    SELECT *
    FROM (
        VALUES (1, 1, 1000.0),
               (2, 1, 2000.0),
               (3, 2, 500.0)
    ) AS o (orderkey, custkey, totalprice)
)
INSERT INTO #customer (custkey, name, total)
SELECT c.custkey, c.name, SUM(o.totalprice) AS total
FROM customer c
JOIN orders o ON c.custkey = o.custkey
WHERE c.nationkey = 1
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 1000000;
SELECT *
FROM #customer
ORDER BY total DESC;
-- REMORPH CLEANUP: DROP TABLE #customer;