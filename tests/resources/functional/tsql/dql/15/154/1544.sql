--Query type: DQL
DECLARE @d datetime2 = '2021-12-08 11:30:15.1234567';
WITH dates AS (
    SELECT @d AS d
)
SELECT 'Year' AS part, DATETRUNC(year, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Quarter' AS part, DATETRUNC(quarter, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Month' AS part, DATETRUNC(month, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Week' AS part, DATETRUNC(week, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Iso_week' AS part, DATETRUNC(iso_week, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'DayOfYear' AS part, DATETRUNC(dayofyear, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Day' AS part, DATETRUNC(day, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Hour' AS part, DATETRUNC(hour, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Minute' AS part, DATETRUNC(minute, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Second' AS part, DATETRUNC(second, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Millisecond' AS part, DATETRUNC(millisecond, d) AS truncated_date
FROM dates
UNION ALL
SELECT 'Microsecond' AS part, DATETRUNC(microsecond, d) AS truncated_date
FROM dates;
