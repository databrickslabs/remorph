--Query type: DDL
CREATE TABLE #t2 (col1 nvarchar(50));
INSERT INTO #t2 (col1)
SELECT 'hello' AS col1;
SELECT * FROM #t2;
-- REMORPH CLEANUP: DROP TABLE #t2;
