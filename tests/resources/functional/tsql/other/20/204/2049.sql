-- tsql sql:
WITH customer_sales AS (
    SELECT o_custkey, SUM(o_totalprice) AS total_sales
    FROM (
        VALUES (1, 100.0),
               (2, 200.0),
               (3, 300.0)
    ) AS orders (o_custkey, o_totalprice)
    GROUP BY o_custkey
)
SELECT c_name, c_address, SUM(cs.total_sales) AS total_sales, RANK() OVER (ORDER BY SUM(cs.total_sales) DESC) AS sales_rank
FROM customer_sales cs
JOIN (
    VALUES (1, 'Customer 1', 'Address 1'),
           (2, 'Customer 2', 'Address 2'),
           (3, 'Customer 3', 'Address 3')
) AS customers (c_custkey, c_name, c_address)
ON cs.o_custkey = customers.c_custkey
WHERE cs.total_sales > 100.0
GROUP BY c_name, c_address
