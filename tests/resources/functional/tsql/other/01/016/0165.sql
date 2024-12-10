-- tsql sql:
WITH temp_table AS (SELECT 1 AS new_column_name, 'value' AS another_column)
SELECT new_column_name, another_column
INTO #temp_table
FROM temp_table;
EXEC sp_rename '#temp_table.new_column_name', 'renamed_column', 'COLUMN';
SELECT *
FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
