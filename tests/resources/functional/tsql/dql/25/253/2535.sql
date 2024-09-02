--Query type: DQL
WITH datetime_values AS (
    SELECT '00:00:01.1234567' AS datetime_value
    UNION ALL
    SELECT '00:00:02.2345678'
    UNION ALL
    SELECT '00:00:03.3456789'
)
SELECT
    DATEPART(millisecond, datetime_value) AS millisecond_part,
    DATEPART(microsecond, datetime_value) AS microsecond_part,
    DATEPART(nanosecond, datetime_value) AS nanosecond_part
FROM datetime_values