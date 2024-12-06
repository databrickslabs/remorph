-- tsql sql:
WITH temp_result AS (SELECT CAST('2022-01-01' AS DATE) AS order_date)
SELECT CONVERT(DATE, order_date) AS order_date
FROM temp_result
