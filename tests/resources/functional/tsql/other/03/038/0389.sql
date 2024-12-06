-- tsql sql:
WITH CustomerCTE AS (
    SELECT *
    FROM dbo.Customer
)
SELECT *
INTO #CustomerClone
FROM CustomerCTE;

SELECT *
FROM #CustomerClone;

-- REMORPH CLEANUP: DROP TABLE #CustomerClone;
