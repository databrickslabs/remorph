--Query type: DCL
WITH TempTable AS ( SELECT 1 AS ID, 'Name1' AS Name UNION ALL SELECT 2, 'Name2' ) SELECT * FROM TempTable;
