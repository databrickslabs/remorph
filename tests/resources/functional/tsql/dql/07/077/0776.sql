-- tsql sql:
SELECT CAST('2016-01-02T23:39:20.123-07:00' AS DATETIME) AS tstamp,
       DATEPART(WEEK, tstamp) AS [WEEK],
       DATEPART(ISOWK, tstamp) AS [WEEK ISO],
       DATEPART(WEEK, tstamp) AS [WEEK OF YEAR],
       DATEPART(YEAR, tstamp) AS [YEAR OF WEEK],
       DATEPART(YEAR, tstamp) AS [YEAR OF WEEK ISO]
FROM (VALUES ('2016-01-02T23:39:20.123-07:00')) AS temp(tstamp);