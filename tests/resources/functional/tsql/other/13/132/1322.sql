--Query type: DDL
WITH customer_orders AS (
    SELECT 1 AS order_key, 'John Doe' AS customer_name, 100.00 AS order_total
    UNION ALL
    SELECT 2, 'Jane Doe', 200.00
    UNION ALL
    SELECT 3, 'Bob Smith', 300.00
)
SELECT *
FROM customer_orders;