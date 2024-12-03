--Query type: DDL
SELECT 'column1' AS a1, 'column2' AS a2 INTO #temp_table;
ALTER TABLE #temp_table DROP COLUMN a1;
SELECT * FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
