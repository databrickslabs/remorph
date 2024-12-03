--Query type: DML
CREATE TABLE #stats (a INT, b INT, stats_stream VARBINARY(MAX));
INSERT INTO #stats (a, b, stats_stream)
SELECT CAST(1 AS INT) AS a, CAST(2 AS INT) AS b, CAST(0x01 AS VARBINARY(MAX)) AS stats_stream;
UPDATE #stats SET stats_stream = 0x01;
SELECT * FROM #stats;
-- REMORPH CLEANUP: DROP TABLE #stats;
