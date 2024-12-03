--Query type: DCL
WITH customer AS (
    SELECT *
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS customer (custkey, name)
),
orders AS (
    SELECT *
    FROM (
        VALUES (1, 1, 1000.0),
               (2, 1, 2000.0),
               (3, 2, 500.0)
    ) AS orders (orderkey, custkey, totalprice)
)
SELECT c.custkey,
       c.name,
       SUM(o.totalprice) AS total_revenue
FROM customer c
JOIN orders o
    ON c.custkey = o.custkey
GROUP BY c.custkey,
         c.name
HAVING SUM(o.totalprice) > 1000
ORDER BY total_revenue DESC;
