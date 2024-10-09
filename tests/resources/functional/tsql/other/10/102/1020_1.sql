--Query type: DDL
CREATE TABLE #CustomerCTE (c_nationkey INT, c_regionkey INT, c_mktsegment VARCHAR(50));
INSERT INTO #CustomerCTE (c_nationkey, c_regionkey, c_mktsegment)
VALUES (1, 1, 'BUILDING'), (2, 2, 'AUTOMOBILE');
CREATE INDEX IX_CN ON #CustomerCTE (c_nationkey, c_regionkey, c_mktsegment DESC);
SELECT * FROM #CustomerCTE;
-- REMORPH CLEANUP: DROP TABLE #CustomerCTE;
-- REMORPH CLEANUP: DROP INDEX IX_CN ON #CustomerCTE;