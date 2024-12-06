-- tsql sql:
SELECT ColC, ColD
INTO #Table2
FROM (
    VALUES (1, 1.0),
           (2, 2.0)
) AS tmp(ColC, ColD);

SELECT *
FROM #Table2;

-- REMORPH CLEANUP: DROP TABLE #Table2;
