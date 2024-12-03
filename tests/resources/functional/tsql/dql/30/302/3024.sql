--Query type: DQL
WITH temp_result AS ( SELECT 'customer' AS [identity], 1 AS [order] UNION ALL SELECT 'order', 2 UNION ALL SELECT 'lineitem', 3 ) SELECT [identity], [order] FROM temp_result ORDER BY [order];
