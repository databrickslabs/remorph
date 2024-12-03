--Query type: DQL
DECLARE @order_date datetime = '1995-03-29 05:06:07.123';
WITH orders AS (
    SELECT 'Order' AS order_type, @order_date AS order_date
),
truncated_orders AS (
    SELECT 'Truncated' AS truncation_type, DATETRUNC(millisecond, order_date) AS truncated_order_date
    FROM orders
)
SELECT *
FROM truncated_orders
