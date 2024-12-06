-- tsql sql:
WITH temp_result AS (SELECT 123.45 AS num)
SELECT STR(FLOOR(num), 8, 3)
FROM temp_result
