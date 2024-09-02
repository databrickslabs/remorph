--Query type: DDL
CREATE TABLE #TempResultQueue (ID INT, Result VARCHAR(100));
INSERT INTO #TempResultQueue (ID, Result)
VALUES (1, 'Result 1'), (2, 'Result 2');
SELECT * FROM #TempResultQueue;
-- REMORPH CLEANUP: DROP TABLE #TempResultQueue;