-- tsql sql:
WITH orders AS (
    SELECT 1 AS order_id, 100 AS order_total, '2020-01-01' AS order_date, 1 AS customer_id, 'Product A' AS product_name
    UNION ALL
    SELECT 2, 200, '2020-01-02', 1, 'Product B'
    UNION ALL
    SELECT 3, 300, '2020-01-03', 2, 'Product C'
)
SELECT
    CASE
        WHEN SUM(CASE WHEN order_total > 100 THEN 1 ELSE 0 END) > 1 THEN 'High'
        ELSE 'Low'
    END AS order_category,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS average_order,
    MAX(order_total) AS max_order,
    MIN(order_total) AS min_order,
    COUNT(DISTINCT customer_id) AS unique_customers,
    STRING_AGG(product_name, ', ') AS products
FROM orders
WHERE order_date >= '2020-01-01'
GROUP BY customer_id
HAVING SUM(order_total) > 50
ORDER BY total_revenue DESC;
