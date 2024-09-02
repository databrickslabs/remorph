--Query type: DDL
WITH models AS (
    SELECT 'model1' AS model_id, 'data1' AS model_data
    UNION ALL
    SELECT 'model2', 'data2'
),
    customers AS (
    SELECT 'customer1' AS customer_id, 10 AS order_total
    UNION ALL
    SELECT 'customer2', 20
),
    predictions AS (
    SELECT c.customer_id, c.order_total, m.model_data AS Prediction
    FROM customers c
    CROSS JOIN models m
    WHERE m.model_id = 1
)
SELECT *
FROM predictions;