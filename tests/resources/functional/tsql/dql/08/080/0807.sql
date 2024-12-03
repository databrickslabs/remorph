--Query type: DQL
WITH temp_result AS ( SELECT 'low' AS price, 'high' AS discount, 'medium' AS size UNION ALL SELECT 'medium' AS price, 'low' AS discount, 'high' AS size ) SELECT 'true' FROM temp_result WHERE price BETWEEN discount AND size
