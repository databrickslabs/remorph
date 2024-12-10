-- tsql sql:
WITH orders AS (
    SELECT *
    FROM (
        VALUES ('1996-01-02', 149814.87, 2982.72, 0.04, 24),
               ('1996-01-02', 149814.87, 2982.72, 0.04, 24),
               ('1996-01-02', 149814.87, 2982.72, 0.04, 24)
    ) AS orders (order_date, total_price, extended_price, discount, quantity)
),
revenue AS (
    SELECT order_date,
           SUM(extended_price * (1 - discount)) AS revenue
    FROM orders
    GROUP BY order_date
)
SELECT CASE
           WHEN SUM(CASE
                      WHEN order_date > '1998-01-01' THEN 1
                      ELSE 0
                  END) > 0 THEN 'After 1998'
           ELSE 'Before 1998'
       END AS order_period,
       COUNT(DISTINCT order_date) AS total_orders,
       MAX(order_date) AS last_order_date,
       MIN(order_date) AS first_order_date
FROM revenue
WHERE order_date BETWEEN '1995-01-01' AND '1999-12-31'
GROUP BY CASE
           WHEN order_date > '1998-01-01' THEN 'After 1998'
           ELSE 'Before 1998'
       END
ORDER BY order_period DESC;
