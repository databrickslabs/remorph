-- tsql sql:
DECLARE @order_date datetime = '2020-02-02 02:02:02.002';
WITH orders AS (
    SELECT 'Order 1' AS order_name, @order_date AS order_date
),
truncated_dates AS (
    SELECT 'Truncated' AS date_type, DATETRUNC(millisecond, order_date) AS truncated_date
    FROM orders
)
SELECT 'Input' AS date_type, order_date
FROM orders
UNION ALL
SELECT date_type, truncated_date
FROM truncated_dates
