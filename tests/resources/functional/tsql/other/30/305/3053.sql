--Query type: DML
CREATE TABLE #TempTable (amount decimal(10, 2));
INSERT INTO #TempTable (amount)
VALUES (100.00), (200.00), (50.00), (75.00), (150.00);
UPDATE STATISTICS #TempTable (amount) WITH INCREMENTAL = ON;
SELECT * FROM #TempTable;
-- REMORPH CLEANUP: DROP TABLE #TempTable;