--Query type: DQL
WITH temp_result AS (
    SELECT 1 AS customer_key, '2022-01-01' AS order_date, 'Shipped' AS status
    UNION ALL
    SELECT 2, '2022-01-02', 'Pending'
    UNION ALL
    SELECT 3, '2022-01-03', 'Shipped'
)
SELECT customer_key, order_date, status
FROM temp_result
WHERE status <> 'Pending' AND status <> 'Cancelled'
ORDER BY order_date, customer_key;