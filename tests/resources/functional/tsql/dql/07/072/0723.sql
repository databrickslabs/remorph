--Query type: DQL
WITH DateCTE AS (
    SELECT CONVERT(DATE, '2019-03-01') AS Date1,
           CONVERT(DATE, '2019-02-01') AS Date2
),
     DateCTE2 AS (
    SELECT CONVERT(DATE, '2019-02-01') AS Date3,
           CONVERT(DATE, '2019-03-01') AS Date4
)
SELECT DATEDIFF(MONTH, Date2, Date1) AS MonthsBetween1,
       DATEDIFF(MONTH, Date4, Date3) AS MonthsBetween2
FROM DateCTE,
     DateCTE2;