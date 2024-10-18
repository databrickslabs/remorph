--Query type: DML
DECLARE @MyCrsrRef CURSOR;

SELECT *
INTO #temp
FROM (
    VALUES (1, 'a'),
           (2, 'b'),
           (3, 'c')
) AS t(id, name);

SET @MyCrsrRef = CURSOR FOR SELECT * FROM #temp;

OPEN @MyCrsrRef;

FETCH NEXT FROM @MyCrsrRef;

CLOSE @MyCrsrRef;

DEALLOCATE @MyCrsrRef;

SELECT *
FROM #temp;

-- REMORPH CLEANUP: DROP TABLE #temp;