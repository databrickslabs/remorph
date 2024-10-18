--Query type: DQL
WITH orders AS (
    SELECT CAST('1992-01-01' AS DATE) AS order_date,
           1 AS order_key
),
     lineitem AS (
    SELECT CAST('1992-01-01' AS DATE) AS ship_date,
           1 AS order_key
)
SELECT DATEADD(day, 10, o.order_date) AS new_order_date,
       DATEADD(day, 20, l.ship_date) AS new_ship_date
FROM orders o
INNER JOIN lineitem l ON o.order_key = l.order_key