-- tsql sql:
WITH TempCTE AS ( SELECT 1 AS Column1, 'Value1' AS Column2 UNION ALL SELECT 2, 'Value2' ) SELECT * FROM TempCTE;
