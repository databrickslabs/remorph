--Query type: DML
WITH dates AS (
    SELECT d
    FROM (
        VALUES ('2022-01-01'), ('2022-01-02'), ('2022-01-03'), ('2022-01-04'), ('2022-01-05'), ('2022-01-06'), ('2022-01-07')
    ) AS dates (d)
)
SELECT
    d AS [Date],
    DATENAME(WEEKDAY, d) AS [Day],
    DATEPART(WEEKDAY, d) AS [DOW],
    DATEADD(WEEK, DATEDIFF(WEEK, 0, d), 0) AS [Trunc Date],
    DATENAME(WEEKDAY, DATEADD(WEEK, DATEDIFF(WEEK, 0, d), 0)) AS [Trunc Day],
    DATEADD(DAY, 6 - DATEPART(WEEKDAY, d), d) AS [Last DOW Date],
    DATENAME(WEEKDAY, DATEADD(DAY, 6 - DATEPART(WEEKDAY, d), d)) AS [Last DOW Day],
    DATEDIFF(WEEK, '2017-01-01', d) AS [Weeks Diff from 2017-01-01 to Date]
FROM dates;
