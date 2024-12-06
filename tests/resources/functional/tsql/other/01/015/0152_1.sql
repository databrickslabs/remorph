-- tsql sql:
DECLARE @week_start INT = 3; -- Monday as the first day of the week
DECLARE @week_of_year_policy INT = 1; -- Not directly applicable in T-SQL, but we'll adjust calculations accordingly

WITH week_data AS (
    SELECT d
    FROM (
        VALUES (
            CONVERT(DATE, '2022-01-01'),
            CONVERT(DATE, '2022-01-08'),
            CONVERT(DATE, '2022-01-15'),
            CONVERT(DATE, '2022-01-22'),
            CONVERT(DATE, '2022-01-29')
        )
    ) AS dates(d)
)
SELECT
    d AS [Date],
    DATENAME(WEEKDAY, d) AS [Day],
    DATEPART(WEEK, d) AS [WOY],
    DATEPART(ISOWK, d) AS [WOY (ISO)],
    YEAR(d) AS [YOW],
    CASE
        WHEN DATEPART(WEEK, d) = 1 AND MONTH(d) = 12 THEN YEAR(d) + 1
        ELSE YEAR(d)
    END AS [YOW (Adjusted)]
FROM week_data;
