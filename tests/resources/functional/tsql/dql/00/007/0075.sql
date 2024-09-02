--Query type: DQL
WITH sales_data AS (
    SELECT 'Product A' AS product_name, 10.99 AS product_price, 100 AS sales_amount
    UNION ALL
    SELECT 'Product B', 9.99, 200
),
    moving_average AS (
    SELECT AVG(sales_amount) AS avg_sales
    FROM sales_data
)
SELECT product_name, product_price, (
    SELECT avg_sales
    FROM moving_average
) AS forecasted_sales
FROM sales_data