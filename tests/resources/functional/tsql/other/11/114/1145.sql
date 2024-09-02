--Query type: DDL
CREATE TABLE #temp_result (xml_data XML);
INSERT INTO #temp_result (xml_data)
VALUES (CAST('<root><book><author>John</author></book></root>' AS XML));
CREATE SELECTIVE XML INDEX idx_xml_data
ON #temp_result(xml_data)
WITH XMLNAMESPACES ('https://www.example.org/' as myns)
FOR ( path1 = '/myns:root/myns:book/myns:author/text()' );
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP INDEX idx_xml_data ON #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;