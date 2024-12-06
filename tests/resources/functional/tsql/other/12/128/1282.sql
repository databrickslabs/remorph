-- tsql sql:
CREATE TABLE #T1 (c1 INT PRIMARY KEY, c2 VARCHAR(50) NULL);
INSERT INTO #T1 (c1, c2)
SELECT c1, c2
FROM (VALUES (1, CONVERT(VARCHAR(50), 'Value1')), (2, CONVERT(VARCHAR(50), 'Value2'))) AS T1(c1, c2);
SELECT c1, c2
FROM #T1;
-- REMORPH CLEANUP: DROP TABLE #T1;
