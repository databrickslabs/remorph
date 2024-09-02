--Query type: DQL
WITH customer_sales AS (
    SELECT *
    FROM (
        VALUES (1, 'Customer#1'),
               (2, 'Customer#2')
    ) AS c (customer_id, customer_name)
),
order_details AS (
    SELECT *
    FROM (
        VALUES (1, 1, 10.0),
               (2, 1, 20.0)
    ) AS o (order_id, customer_id, order_total)
)
SELECT cs.customer_name,
       od.order_total
FROM customer_sales AS cs
INNER JOIN order_details AS od
    ON cs.customer_id = od.customer_id
WHERE od.order_id IS NOT NULL
      AND cs.customer_name = 'Customer#1';