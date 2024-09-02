--Query type: DQL
WITH temp_result AS (
    SELECT 10 AS customer_key, 20 AS order_key, 30 AS line_number
    UNION ALL
    SELECT 40, 50, 60
    UNION ALL
    SELECT 70, 80, NULL
)
SELECT customer_key, order_key, line_number, IIF(line_number IS NULL, IIF(customer_key < order_key, customer_key, order_key), IIF(customer_key < order_key, IIF(customer_key < line_number, customer_key, line_number), IIF(order_key < line_number, order_key, line_number))) AS smallest_value
FROM temp_result