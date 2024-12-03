--Query type: DQL
WITH cte AS (SELECT '2007-05-10 00:00:01.1234567 +05:10' AS datetime_value)
SELECT DATEPART(tzoffset, TRY_CAST(datetime_value AS datetimeoffset)) AS tzoffset
FROM cte
