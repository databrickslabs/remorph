--Query type: DQL
WITH temp_result AS (SELECT CAST('12:12:12.1234567' AS time) AS d)
SELECT DATETRUNC(year, d)
FROM temp_result
