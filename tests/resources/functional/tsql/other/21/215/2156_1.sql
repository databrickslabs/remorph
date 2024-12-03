--Query type: DDL
CREATE TABLE #TempTable (xml_column XML);
INSERT INTO #TempTable (xml_column)
VALUES (CONVERT(XML, '<root><comment>test</comment></root>'));
CREATE PRIMARY XML INDEX PXML_Temp_CTE
ON #TempTable (xml_column)
WITH (XML_COMPRESSION = ON);
SELECT *
FROM #TempTable;
-- REMORPH CLEANUP: DROP TABLE #TempTable;
