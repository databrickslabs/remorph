--Query type: DML
WITH customer_load AS (
    SELECT 'customer1' AS customer_name, 100 AS load_value
    UNION ALL
    SELECT 'customer2' AS customer_name, 200 AS load_value
),
    sales_load AS (
    SELECT 'sales1' AS sales_name, 500 AS sales_value
    UNION ALL
    SELECT 'sales2' AS sales_name, 600 AS sales_value
)
SELECT *
FROM customer_load;

SELECT *
FROM sales_load;
