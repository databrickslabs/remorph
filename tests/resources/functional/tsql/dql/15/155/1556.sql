--Query type: DQL
DECLARE @order_date DATETIME2 = '2020-04-15 21:22:11';
WITH orders AS (
    SELECT CAST('2020-04-15 21:22:11' AS DATETIME2) AS order_date
)
SELECT DATE_BUCKET(WEEK, 1, order_date)
FROM orders;
