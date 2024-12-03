--Query type: DCL
WITH WaitTimes AS (
    SELECT 1 AS seconds, 'SECONDS' AS unit
    UNION ALL
    SELECT 2 * 60, 'MINUTES'
    UNION ALL
    SELECT 3 * 60 * 60, 'HOURS'
)
SELECT 'WAITFOR DELAY ''' + CONVERT(VARCHAR, seconds) + ' SECONDS''' AS query
INTO #WaitQueries
FROM WaitTimes;

DECLARE @query VARCHAR(100);

DECLARE cur CURSOR FOR SELECT query FROM #WaitQueries;

OPEN cur;

FETCH NEXT FROM cur INTO @query;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC (@query);
    FETCH NEXT FROM cur INTO @query;
END

CLOSE cur;

DEALLOCATE cur;

-- REMORPH CLEANUP: DROP TABLE #WaitQueries;
