-- tsql sql:
WITH dates AS (
    SELECT '2016-01-02T23:39:20.123-07:00' AS date_str
)
SELECT CAST(date_str AS DATETIME) AS tstamp,
       DATEPART(WEEKDAY, CAST(date_str AS DATETIME)) AS [DAY OF WEEK],
       DATEPART(ISOWW, CAST(date_str AS DATETIME)) AS [DAY OF WEEK ISO]
FROM dates;
