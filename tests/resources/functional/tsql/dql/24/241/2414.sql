-- tsql sql:
WITH temp_result AS (SELECT 1.00 AS value)
SELECT ASIN(value) AS asinCalc
FROM temp_result
