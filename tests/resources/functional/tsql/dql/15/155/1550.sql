--Query type: DQL
DECLARE @order_date DATE = '1995-01-01';
WITH temp_result AS (
    SELECT @order_date AS [Order Date], '1995-01-01' AS [Lineitem Ship Date]
)
SELECT *
FROM temp_result
