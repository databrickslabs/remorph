--Query type: DCL
CREATE TABLE #TempResult (ID INT, Name VARCHAR(50));
INSERT INTO #TempResult (ID, Name)
VALUES (1, 'Value1'), (2, 'Value2');
SELECT * FROM #TempResult;
DROP TABLE #TempResult;
-- REMORPH CLEANUP: DROP TABLE #TempResult;
