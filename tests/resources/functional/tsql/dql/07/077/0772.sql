--Query type: DQL
WITH dates AS (
    SELECT '2013-05-08T23:39:20.123-07:00' AS tstamp
)
SELECT
    tstamp AS tstamp,
    DATEPART(YEAR, tstamp) AS [YEAR],
    DATENAME(QUARTER, tstamp) AS [QUARTER OF YEAR],
    DATEPART(MONTH, tstamp) AS [MONTH],
    DATEPART(DAY, tstamp) AS [DAY],
    DATEPART(DAY, tstamp) AS [DAY OF MONTH],
    DATEPART(DAYOFYEAR, tstamp) AS [DAY OF YEAR]
FROM dates;
