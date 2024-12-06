-- tsql sql:
WITH dates AS (
  SELECT CAST('2022-01-01' AS DATE) AS d
  UNION ALL
  SELECT DATEADD(day, 1, d)
  FROM dates
  WHERE d < '2022-01-31'
)
SELECT
  d AS [Date],
  DATENAME(WEEKDAY, d) AS [Day],
  DATEPART(WEEKDAY, d) AS [DOW],
  DATEADD(day, -DATEPART(WEEKDAY, d) + 1, d) AS [Trunc Date],
  DATENAME(WEEKDAY, DATEADD(day, -DATEPART(WEEKDAY, d) + 1, d)) AS [Trunc Day],
  DATEADD(day, 7 - DATEPART(WEEKDAY, d), d) AS [Last DOW Date],
  DATENAME(WEEKDAY, DATEADD(day, 7 - DATEPART(WEEKDAY, d), d)) AS [Last DOW Day],
  DATEDIFF(WEEK, '2022-01-01', d) AS [Weeks Diff from 2022-01-01 to Date]
FROM dates
OPTION (MAXRECURSION 0);
