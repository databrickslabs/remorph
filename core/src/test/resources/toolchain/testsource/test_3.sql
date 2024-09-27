-- ## WITH XMLWORKSPACES
--
-- Databricks SQL does not currently support XML workspaces, so for now, we cover the syntax without recommending
-- a translation.
--
-- tsql sql:
WITH XMLNAMESPACES ('somereference' as namespace)
SELECT col1 as 'namespace:col1',
       col2 as 'namespace:col2'
FROM  Table1
WHERE col2 = 'xyz'
FOR XML RAW ('namespace:namespace'), ELEMENTS;
