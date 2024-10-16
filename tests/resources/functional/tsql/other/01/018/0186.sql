--Query type: DDL
CREATE TABLE #cte (c_custkey INT, c_name VARCHAR(10));
INSERT INTO #cte
SELECT *
FROM (VALUES (1, 'a'), (2, 'b')) AS t (c_custkey, c_name);
SELECT *
FROM #cte;
-- REMORPH CLEANUP: DROP TABLE #cte;