--Query type: DML
CREATE TABLE #t1 (col1 INT, col2 INT);
INSERT INTO #t1 (col1, col2)
SELECT a, b
FROM (
    SELECT a = 1, b = 2, c = 11
) src
WHERE c > 10;
SELECT * FROM #t1;
-- REMORPH CLEANUP: DROP TABLE #t1;