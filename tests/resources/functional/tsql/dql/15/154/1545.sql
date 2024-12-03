--Query type: DQL
WITH temp_result AS (SELECT CAST('2021-12-12 12:12:12.12345' AS datetime2(3)) AS d)
SELECT DATETRUNC(microsecond, d)
FROM temp_result
