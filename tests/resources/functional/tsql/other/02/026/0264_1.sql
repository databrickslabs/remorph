--Query type: DDL
CREATE TABLE #demo_temporary (i INTEGER);
INSERT INTO #demo_temporary (i)
SELECT i
FROM (
    VALUES (1), (2), (3)
) AS demo_temporary_table (i);
CREATE TABLE #demo_temp (i INTEGER);
INSERT INTO #demo_temp (i)
SELECT i
FROM (
    VALUES (4), (5), (6)
) AS demo_temp_table (i);
SELECT *
FROM #demo_temporary;
SELECT *
FROM #demo_temp;
-- REMORPH CLEANUP: DROP TABLE #demo_temporary;
-- REMORPH CLEANUP: DROP TABLE #demo_temp;