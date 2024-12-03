--Query type: DDL
WITH orders AS (
    SELECT 1000 AS order_total, '2020-01-01' AS order_date, 1 AS customer_id, 'Product A' AS product_name
    UNION ALL
    SELECT 2000, '2020-01-02', 2, 'Product B'
    UNION ALL
    SELECT 3000, '2020-01-03', 3, 'Product C'
)
SELECT TOP 10
    CASE
        WHEN SUM(CASE WHEN order_total > 1000 THEN 1 ELSE 0 END) > 10 THEN 'High'
        ELSE 'Low'
    END AS order_category,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS avg_order_value,
    MAX(order_total) AS max_order_value,
    MIN(order_total) AS min_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_total) AS total_orders,
    STRING_AGG(product_name, ', ') AS products
FROM orders
WHERE order_date >= '2020-01-01'
GROUP BY customer_id
HAVING SUM(order_total) > 5000
ORDER BY total_revenue DESC;
