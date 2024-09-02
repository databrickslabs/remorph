--Query type: DQL
WITH temp_result AS ( SELECT -1.0 AS num UNION ALL SELECT 0.0 UNION ALL SELECT 1.0 ) SELECT ABS(num) FROM temp_result