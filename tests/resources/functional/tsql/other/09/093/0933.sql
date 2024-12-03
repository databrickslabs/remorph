--Query type: DDL
WITH customers AS (
    SELECT custkey, name, nationkey
    FROM (
        VALUES (1, 'Customer 1', 1),
               (2, 'Customer 2', 2)
    ) AS c (custkey, name, nationkey)
),
orders AS (
    SELECT orderkey, custkey, totalprice, orderdate
    FROM (
        VALUES (1, 1, 100.0, '1995-01-01'),
               (2, 1, 200.0, '1995-01-02')
    ) AS o (orderkey, custkey, totalprice, orderdate)
)
SELECT TOP 10 c.custkey, c.name, SUM(o.totalprice) AS total_order_value
FROM customers c
JOIN orders o ON c.custkey = o.custkey
WHERE c.nationkey = 1 AND o.orderdate >= '1995-01-01'
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 100000
ORDER BY total_order_value DESC;
