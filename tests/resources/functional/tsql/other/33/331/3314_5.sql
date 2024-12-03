--Query type: DML
CREATE TABLE #TempTable (ID INT, Name VARCHAR(50), Age INT);

WITH TempCTE AS (
    SELECT 1 AS ID, 'Unknown' AS Name, 0 AS Age
)
INSERT INTO #TempTable (ID, Name, Age)
SELECT ID, Name, Age
FROM TempCTE;

SELECT *
FROM #TempTable;

-- REMORPH CLEANUP: DROP TABLE #TempTable;
