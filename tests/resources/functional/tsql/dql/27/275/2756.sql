--Query type: DQL
WITH temp_result AS ( SELECT 1.00 AS value UNION ALL SELECT 10.00 AS value UNION ALL SELECT 100.00 AS value ) SELECT SQRT(value) AS square_root FROM temp_result