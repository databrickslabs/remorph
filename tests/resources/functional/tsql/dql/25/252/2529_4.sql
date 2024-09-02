--Query type: DQL
WITH dates AS (SELECT '2005-12-31 23:59:59.9999999' AS start_date, '2006-01-01 00:00:00.0000000' AS end_date)
SELECT DATEDIFF(hour, start_date, end_date)
FROM dates