-- tsql sql:
WITH time_values AS (
    SELECT CAST('07:35' AS time) AS time_value
    UNION ALL
    SELECT CAST('12:00' AS time) AS time_value
    UNION ALL
    SELECT CAST('15:45' AS time) AS time_value
)
SELECT FORMAT(time_value, N'hh:mm') AS formatted_time
FROM time_values;
