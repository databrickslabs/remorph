-- tsql sql:
WITH customer_sales AS (
    SELECT c_custkey, c_name, SUM(o_totalprice) AS total_sales
    FROM (
        VALUES (1, 'Customer1', 100.0),
               (2, 'Customer2', 200.0),
               (3, 'Customer3', 300.0)
    ) AS customer (c_custkey, c_name, o_totalprice)
    GROUP BY c_custkey, c_name
)
SELECT *
FROM customer_sales;
