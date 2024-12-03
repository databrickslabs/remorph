--Query type: DQL
WITH dates AS (
    SELECT CAST('2005-12-31 23:59:59.9999999' AS datetime) AS start_date,
           CAST('2006-01-01 00:00:00.0000000' AS datetime) AS end_date
)
SELECT DATEDIFF_BIG(year, start_date, end_date) AS year_diff,
       DATEDIFF_BIG(quarter, start_date, end_date) AS quarter_diff,
       DATEDIFF_BIG(month, start_date, end_date) AS month_diff,
       DATEDIFF_BIG(dayofyear, start_date, end_date) AS dayofyear_diff,
       DATEDIFF_BIG(day, start_date, end_date) AS day_diff,
       DATEDIFF_BIG(week, start_date, end_date) AS week_diff,
       DATEDIFF_BIG(hour, start_date, end_date) AS hour_diff,
       DATEDIFF_BIG(minute, start_date, end_date) AS minute_diff,
       DATEDIFF_BIG(second, start_date, end_date) AS second_diff,
       DATEDIFF_BIG(millisecond, start_date, end_date) AS millisecond_diff
FROM dates
