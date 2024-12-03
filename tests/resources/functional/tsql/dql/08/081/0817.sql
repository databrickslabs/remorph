--Query type: DQL
WITH temp_result AS ( SELECT 'California' AS region, 'USA' AS country UNION ALL SELECT 'New York', 'USA' UNION ALL SELECT 'London', 'UK' ) SELECT region, country FROM temp_result ORDER BY region;
