--Query type: DQL
WITH temp_result AS (SELECT CAST(-0.0 AS FLOAT) AS float_value)
SELECT CAST(float_value AS BIT)
FROM temp_result
