--Query type: DQL
DECLARE @dt datetimeoffset = switchoffset(CONVERT(datetimeoffset, GETDATE()), '-04:00');
WITH temp_result AS (
    SELECT GETDATE() AS orderdate, 100.0 AS totalprice
)
SELECT *
FROM temp_result
WHERE orderdate > @dt
OPTION (RECOMPILE);
