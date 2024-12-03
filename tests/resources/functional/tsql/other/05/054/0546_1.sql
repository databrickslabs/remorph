--Query type: DDL
WITH total_orders AS (
    SELECT custkey, totalprice, ROW_NUMBER() OVER (PARTITION BY custkey ORDER BY totalprice DESC) AS row_num
    FROM (
        VALUES (1, 1000.0),
               (1, 2000.0),
               (2, 3000.0),
               (3, 4000.0)
    ) AS orders (custkey, totalprice)
),
     customer_totals AS (
    SELECT custkey, SUM(totalprice) AS total
    FROM total_orders
    GROUP BY custkey
),
     customers AS (
    SELECT *
    FROM (
        VALUES (1, 'Customer 1'),
               (2, 'Customer 2'),
               (3, 'Customer 3')
    ) AS customers (custkey, name)
)
SELECT c.custkey, c.name, ct.total AS total
FROM customers c
JOIN customer_totals ct ON c.custkey = ct.custkey
WHERE c.custkey = 1
ORDER BY ct.total DESC;
