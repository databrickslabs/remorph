-- tsql sql:
WITH temp_result AS (SELECT @@TIMETICKS AS time_ticks)
SELECT time_ticks AS [Time Ticks]
FROM temp_result;
