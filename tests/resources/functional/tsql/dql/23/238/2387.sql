--Query type: DQL
WITH temp_result AS (
    SELECT 1 AS io_busy, 2 AS time_ticks
)
SELECT (
    temp_result.io_busy * temp_result.time_ticks
) * 1000 AS [IO microseconds],
    GETDATE() AS [as of]
FROM temp_result;