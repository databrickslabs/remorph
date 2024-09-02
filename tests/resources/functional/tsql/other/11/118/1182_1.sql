--Query type: DDL
WITH TempTable AS (SELECT * FROM (VALUES (1, 'John'), (2, 'Doe')) AS TempTable(ID, Name))
SELECT *
FROM TempTable;