--Query type: DQL
DECLARE @orderdate datetime2 = '1995-01-01 00:00:00.0000000';
WITH orders AS (
  SELECT 'year' AS period, DATEADD(year, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'quarter' AS period, DATEADD(quarter, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'month' AS period, DATEADD(month, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'dayofyear' AS period, DATEADD(dayofyear, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'day' AS period, DATEADD(day, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'week' AS period, DATEADD(week, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'weekday' AS period, DATEADD(weekday, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'hour' AS period, DATEADD(hour, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'minute' AS period, DATEADD(minute, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'second' AS period, DATEADD(second, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'millisecond' AS period, DATEADD(millisecond, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'microsecond' AS period, DATEADD(microsecond, 1, @orderdate) AS orderdate
  UNION ALL
  SELECT 'nanosecond' AS period, DATEADD(nanosecond, 1, @orderdate) AS orderdate
)
SELECT * FROM orders;
