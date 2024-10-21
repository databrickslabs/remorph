--Query type: DDL
ALTER DATABASE [database_name]
SET READ_WRITE;

WITH orders AS (
    SELECT 1000 AS order_total, 1 AS order_id, '2020-01-01' AS order_date
    UNION ALL
    SELECT 2000, 2, '2020-01-02'
    UNION ALL
    SELECT 3000, 3, '2020-01-03'
)

SELECT
    CASE
        WHEN SUM(CASE WHEN order_total > 1000 THEN 1 ELSE 0 END) > 0 THEN 'High'
        ELSE 'Low'
    END AS order_category,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS average_order,
    MAX(order_total) AS max_order,
    MIN(order_total) AS min_order,
    COUNT(DISTINCT order_id) AS num_orders,
    COUNT(order_id) AS total_orders,
    GROUPING(order_id) AS order_id_grouping,
    GROUPING(order_total) AS order_total_grouping

FROM orders

WHERE order_date >= '2020-01-01'

GROUP BY order_id, order_total

HAVING SUM(order_total) > 1000

ORDER BY total_revenue DESC

OFFSET 5 ROWS

FETCH NEXT 10 ROWS ONLY;