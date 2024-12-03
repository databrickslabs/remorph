--Query type: DQL
WITH dates AS (
    SELECT CONVERT(datetime, '2017-01-01 12:00:00') AS date_value
    UNION ALL
    SELECT CONVERT(datetime, '2018-01-01 12:00:00')
    UNION ALL
    SELECT CONVERT(datetime, '2019-01-01 12:00:00')
)
SELECT DATEADD(MONTH, 6, date_value) AS new_date
FROM dates;
