-- tsql sql:
DECLARE @dt datetimeoffset = switchoffset(CONVERT(datetimeoffset, GETDATE()), '-04:00');
WITH temp_result AS (
    SELECT '2022-01-01' AS orderdate, 100.00 AS totalamount
    UNION ALL
    SELECT '2022-01-02', 200.00
)
SELECT *
FROM temp_result
WHERE orderdate > @dt
OPTION (RECOMPILE);
