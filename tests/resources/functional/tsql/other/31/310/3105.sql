--Query type: TCL
WITH revenue AS (
    SELECT orders.order_id,
           customers.customer_name,
           SUM(orders.order_total) AS total_revenue
    FROM (
        VALUES (1, 100, '2020-01-01', 1000.0),
               (2, 200, '2020-01-15', 2000.0),
               (3, 100, '2020-02-01', 1500.0)
    ) AS orders (
        order_id,
        customer_id,
        order_date,
        order_total
    )
    INNER JOIN (
        VALUES (100, 'Customer 1'),
               (200, 'Customer 2')
    ) AS customers (
        customer_id,
        customer_name
    ) ON orders.customer_id = customers.customer_id
    GROUP BY orders.order_id,
             customers.customer_name
)
SELECT *,
       ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS row_num
FROM revenue
WHERE total_revenue > 1000
ORDER BY total_revenue DESC;