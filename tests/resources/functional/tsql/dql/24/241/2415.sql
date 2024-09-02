--Query type: DQL
WITH temp_result AS (SELECT 1.1472738 AS value)
SELECT ASIN(value) AS asinCalc
FROM temp_result;