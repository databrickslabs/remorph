--Query type: DDL
CREATE TABLE #temp (col1 INT);
WITH tempCTE AS (SELECT 1 AS col1)
INSERT INTO #temp (col1)
SELECT col1 FROM tempCTE;
SELECT * FROM #temp;
