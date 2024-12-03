--Query type: DQL
WITH temp_result AS (SELECT '2022-01-01' AS order_date)
SELECT CONVERT(DATE, order_date) AS [Date-Interpretation-of-input-format]
FROM temp_result
