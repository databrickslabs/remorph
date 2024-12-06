-- tsql sql:
WITH sales_data AS (
    SELECT 'John' AS salesperson_name, 1000 AS sales_in_dollars
    UNION ALL
    SELECT 'Alice', 800
    UNION ALL
    SELECT 'Bob', 1200
)
SELECT salesperson_name, sales_in_dollars, RANK() OVER (ORDER BY sales_in_dollars DESC) AS sales_rank
FROM sales_data
ORDER BY sales_rank;