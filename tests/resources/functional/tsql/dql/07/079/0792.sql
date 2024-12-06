-- tsql sql:
WITH temp_result AS (
    SELECT CAST('2013-05-08T23:39:20.123-07:00' AS DATETIME) AS tstamp
)
SELECT tstamp AS TSTAMP, DATEPART(HOUR, tstamp) AS [HOUR], DATEPART(MINUTE, tstamp) AS [MINUTE], DATEPART(SECOND, tstamp) AS [SECOND]
FROM temp_result;
