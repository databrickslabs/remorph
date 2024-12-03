--Query type: DQL
WITH dates AS (
    SELECT CAST('2022-01-01' AS DATE) AS date_value
)
SELECT TOP 1
    YEAR(date_value) AS year_value,
    MONTH(date_value) AS month_value,
    DAY(date_value) AS day_value
FROM dates;
