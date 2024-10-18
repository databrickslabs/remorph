--Query type: DQL
DECLARE @date VARCHAR(255) = '12/1/2011';
WITH customer_orders AS (
    SELECT '12/1/2011' AS order_date
)
SELECT EOMONTH(order_date) AS Result
FROM customer_orders;