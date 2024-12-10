-- tsql sql:
WITH temp_result AS (SELECT 5 AS value)
SELECT POWER(10, LOG10(value)) AS result
FROM temp_result
