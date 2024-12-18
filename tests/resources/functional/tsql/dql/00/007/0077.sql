-- tsql sql:
WITH forecast_data AS (
    SELECT CAST(o.o_orderdate AS DATE) AS order_date,
           SUM(l.ol_quantity) AS quantity
    FROM orders o
    INNER JOIN lineitem l ON o.o_orderkey = l.l_orderkey
    GROUP BY CAST(o.o_orderdate AS DATE)
),

moving_average AS (
    SELECT order_date,
           quantity,
           AVG(quantity) OVER (ORDER BY order_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS moving_avg
    FROM forecast_data
)

SELECT order_date,
       quantity,
       moving_avg AS forecast
FROM moving_average
ORDER BY order_date;
