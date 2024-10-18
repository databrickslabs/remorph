--Query type: DDL
WITH sales_data AS (
    SELECT 'Europe' AS region, 1000 AS sales
    UNION ALL
    SELECT 'Europe', 2000
    UNION ALL
    SELECT 'Asia', 500
    UNION ALL
    SELECT 'Asia', 3000
)
SELECT
    CASE
        WHEN SUM(CASE WHEN region = 'Europe' THEN sales ELSE 0 END) > SUM(CASE WHEN region = 'Asia' THEN sales ELSE 0 END) THEN 'Europe has more total sales'
        WHEN SUM(CASE WHEN region = 'Europe' THEN sales ELSE 0 END) < SUM(CASE WHEN region = 'Asia' THEN sales ELSE 0 END) THEN 'Asia has more total sales'
        ELSE 'Europe and Asia have the same total sales'
    END AS result
FROM sales_data;