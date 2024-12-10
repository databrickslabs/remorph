-- tsql sql:
WITH revenue AS (
    SELECT 1 AS order_id, 'Customer1' AS customer_name, 1000.0 AS total_revenue
    UNION ALL
    SELECT 2 AS order_id, 'Customer2' AS customer_name, 2000.0 AS total_revenue
)
SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_name ORDER BY total_revenue DESC) AS row_num
FROM revenue
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM revenue
)
ORDER BY total_revenue DESC;
