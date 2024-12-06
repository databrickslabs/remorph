-- tsql sql:
WITH MyNewTable AS (
    SELECT 0 AS orderKey, CAST('' AS nvarchar) AS orderStatus
)
SELECT *
INTO #MyNewTable
FROM MyNewTable;

SELECT *
FROM #MyNewTable;

-- REMORPH CLEANUP: DROP TABLE #MyNewTable;
