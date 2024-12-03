--Query type: DQL
WITH temp_result AS (SELECT CAST('1992-01-01' AS date) AS order_date)
SELECT DATETRUNC(week, order_date)
FROM temp_result
