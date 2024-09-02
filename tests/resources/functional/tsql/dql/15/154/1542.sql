--Query type: DQL
DECLARE @order_date datetime2 = '1998-12-11 02:03:04.1234567';
WITH orders AS (
    SELECT '1998-12-11 02:03:04.1234567' AS order_date
)
SELECT DATETRUNC(day, @order_date) AS truncated_date
FROM orders