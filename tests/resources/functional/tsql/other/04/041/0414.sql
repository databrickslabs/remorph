--Query type: DDL
DECLARE @StringPartitionFunction nvarchar(max) = N'CREATE PARTITION FUNCTION StringPartitionFunction (nvarchar(50)) AS RANGE RIGHT FOR VALUES (';
WITH Characters AS (
    SELECT CONVERT(nvarchar(1), N'a') AS CharValue, 1 AS Level
    UNION ALL
    SELECT CONVERT(nvarchar(1), NCHAR(UNICODE(CharValue) + 1)), Level + 1
    FROM Characters
    WHERE Level < 14999
)
SELECT @StringPartitionFunction += N'''' + CharValue + N''', '
FROM Characters
OPTION (MAXRECURSION 0);
SET @StringPartitionFunction += N'''' + NCHAR(UNICODE('a') + 14999) + N'''' + N');';
EXEC sp_executesql @StringPartitionFunction;
-- REMORPH CLEANUP: DROP PARTITION FUNCTION StringPartitionFunction;