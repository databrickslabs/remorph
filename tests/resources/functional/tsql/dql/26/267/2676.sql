--Query type: DQL
WITH customer_data AS (
    SELECT 'Customer1' AS customer_name, 1 AS customer_id
    UNION ALL
    SELECT 'Customer2' AS customer_name, 2 AS customer_id
),
orders_data AS (
    SELECT 1 AS order_id, 1 AS customer_id, '2020-01-01' AS order_date
    UNION ALL
    SELECT 2 AS order_id, 2 AS customer_id, '2020-01-15' AS order_date
)
SELECT c.customer_name, o.order_id, o.order_date
FROM customer_data c
INNER JOIN orders_data o ON c.customer_id = o.customer_id;