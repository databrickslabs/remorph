--Query type: DQL
WITH time_values AS (
    SELECT CAST('07:35' AS time) AS time_value
)
SELECT FORMAT(time_value, N'hh.mm') AS formatted_time
FROM time_values;