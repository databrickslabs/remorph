--Query type: DDL
WITH SalesData AS (
    SELECT 20220101 AS [date], 1 AS [product], 1 AS [store], 10 AS [quantity], 100.00 AS [price], 1000.00 AS [amount]
    UNION ALL
    SELECT 20220102 AS [date], 2 AS [product], 2 AS [store], 20 AS [quantity], 200.00 AS [price], 2000.00 AS [amount]
),
ProductsData AS (
    SELECT 1 AS [product_id], 'Product A' AS [product_name], 'Category A' AS [product_category]
    UNION ALL
    SELECT 2 AS [product_id], 'Product B' AS [product_name], 'Category B' AS [product_category]
)
SELECT
    CASE
        WHEN T1.[date] > 20220101 THEN 'Recent'
        ELSE 'Old'
    END AS [Sales Period],
    T1.[product],
    T1.[store],
    T1.[quantity],
    T1.[price],
    T1.[amount],
    T2.[product_name],
    T2.[product_category]
FROM
    SalesData AS T1
    INNER JOIN ProductsData AS T2 ON T1.[product] = T2.[product_id]
WHERE
    T1.[date] > 20220101
ORDER BY
    T1.[date] DESC