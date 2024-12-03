--Query type: DDL
DECLARE @sql nvarchar(max) = 'CREATE TABLE #TempTable (id int, column1 int); INSERT INTO #TempTable SELECT id, column1 FROM (VALUES (1, 10), (2, 30), (3, 50)) AS TempTable(id, column1); ALTER TABLE #TempTable DROP COLUMN column1;'; EXEC sp_executesql @sql;
