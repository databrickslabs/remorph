--Query type: DDL
CREATE TABLE #TempTable (id INT, xmlcol XML);
INSERT INTO #TempTable (id, xmlcol)
VALUES (1, '<root><path>value</path></root>');
CREATE PRIMARY XML INDEX sxi_index_temp
ON #TempTable(xmlcol);
CREATE XML INDEX filt_sxi_index_d
ON #TempTable(xmlcol)
USING XML INDEX sxi_index_temp
FOR (path);
SELECT *
FROM #TempTable;
-- REMORPH CLEANUP: DROP TABLE #TempTable;
-- REMORPH CLEANUP: DROP INDEX sxi_index_temp
ON #TempTable;
-- REMORPH CLEANUP: DROP INDEX filt_sxi_index_d
ON #TempTable;