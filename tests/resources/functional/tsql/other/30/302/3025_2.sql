-- tsql sql:
CREATE TABLE #TestTable (ID INT, String VARCHAR(30));
INSERT INTO #TestTable (ID, String)
SELECT * FROM (VALUES (1, 'Test')) AS CTE(ID, String);

SELECT * FROM #TestTable;
-- REMORPH CLEANUP: DROP TABLE #TestTable;
