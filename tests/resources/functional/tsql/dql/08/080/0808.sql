--Query type: DQL
WITH temp_result AS ( SELECT 1 AS num ) SELECT 'true' FROM temp_result WHERE num BETWEEN 0 AND 10;