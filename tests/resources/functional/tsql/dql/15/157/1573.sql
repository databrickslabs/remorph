--Query type: DQL
DECLARE @orderdate datetime2;
SET @orderdate = '1992-01-01 01:01:01.1111111';
WITH orders AS (
    SELECT 1 AS orderkey, @orderdate AS orderdate
)
SELECT
    DATEADD(quarter, 4, orderdate) AS quarter_add,
    DATEADD(month, 13, orderdate) AS month_add,
    DATEADD(dayofyear, 365, orderdate) AS dayofyear_add,
    DATEADD(day, 365, orderdate) AS day_add,
    DATEADD(week, 5, orderdate) AS week_add,
    DATEADD(weekday, 31, orderdate) AS weekday_add,
    DATEADD(hour, 23, orderdate) AS hour_add,
    DATEADD(minute, 59, orderdate) AS minute_add,
    DATEADD(second, 59, orderdate) AS second_add,
    DATEADD(millisecond, 1, orderdate) AS millisecond_add
FROM orders