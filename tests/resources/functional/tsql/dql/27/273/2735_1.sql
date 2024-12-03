--Query type: DQL
WITH temp_result AS (SELECT 150.75 AS decimal_value)
SELECT ROUND(decimal_value, 0, 1) AS rounded_value
FROM temp_result;
