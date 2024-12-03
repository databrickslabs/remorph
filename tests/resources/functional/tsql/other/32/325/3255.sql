--Query type: DDL
CREATE FULLTEXT CATALOG ftCatalog AS DEFAULT;

WITH orders AS (
    SELECT 1000 AS order_total, '2020-01-01' AS order_date, 1 AS customer_id, 'Product A' AS product_name
    UNION ALL
    SELECT 2000, '2020-01-15', 2, 'Product B'
    UNION ALL
    SELECT 500, '2020-02-01', 1, 'Product C'
)

SELECT
    CASE
        WHEN SUM(CASE WHEN order_total > 1000 THEN 1 ELSE 0 END) > 1 THEN 'High'
        ELSE 'Low'
    END AS order_category,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS avg_order_value,
    MAX(order_total) AS max_order_value,
    MIN(order_total) AS min_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_orders,
    STRING_AGG(product_name, ', ') AS products
FROM orders
WHERE order_date >= '2020-01-01'
GROUP BY customer_id
HAVING SUM(order_total) > 500
ORDER BY total_revenue DESC
