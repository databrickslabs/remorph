--Query type: DQL
WITH temp_result AS (SELECT '2022-01-01' AS date_string)
SELECT CONVERT(DATE, date_string) AS [Converted-Date]
FROM temp_result