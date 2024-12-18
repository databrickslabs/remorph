-- tsql sql:
WITH customer_sales AS (
    SELECT c_name, SUM(o_totalprice) AS total_sales
    FROM (
        VALUES ('Customer#0001', 100.0),
               ('Customer#0002', 200.0),
               ('Customer#0003', 300.0)
    ) AS customers (c_name, o_totalprice)
    GROUP BY c_name
)
SELECT *
FROM customer_sales;
