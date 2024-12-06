-- tsql sql:
WITH SalesCTE AS (
    SELECT product_id, SUM(sales_amount) AS total_sales
    FROM (
        VALUES (1, 100.00), (2, 200.00), (3, 300.00), (1, 150.00), (2, 250.00)
    ) AS SalesData (product_id, sales_amount)
    GROUP BY product_id
),
ColumnsCTE AS (
    SELECT 'product_id' AS column_name, 'int' AS data_type
    UNION ALL
    SELECT 'total_sales', 'decimal'
)
SELECT s.product_id, s.total_sales, c.column_name, c.data_type, LEN(c.column_name) AS column_name_length
FROM SalesCTE s
INNER JOIN ColumnsCTE c ON s.product_id = 1
WHERE s.total_sales > 200.00
ORDER BY s.product_id;
