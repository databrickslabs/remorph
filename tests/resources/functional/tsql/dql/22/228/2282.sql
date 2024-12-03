--Query type: DQL
WITH temp_result AS (SELECT 'test' AS test_value)
SELECT CASE WHEN TRY_CAST(test_value AS FLOAT) IS NULL THEN 'Cast failed' ELSE 'Cast succeeded' END AS Result
FROM temp_result
