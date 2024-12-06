-- tsql sql:
WITH NewExternalTable AS ( SELECT 1 AS column1, 'value1' AS column2 UNION ALL SELECT 2, 'value2' ) SELECT * FROM NewExternalTable;
