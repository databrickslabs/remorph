--Query type: DDL
CREATE TABLE #CustomerIndex (c_name VARCHAR(50) UNIQUE);
INSERT INTO #CustomerIndex (c_name)
VALUES ('Customer1'), ('Customer2'), ('Customer3');
SELECT * FROM #CustomerIndex;
-- REMORPH CLEANUP: DROP TABLE #CustomerIndex;
