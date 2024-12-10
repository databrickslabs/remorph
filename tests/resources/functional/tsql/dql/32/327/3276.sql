-- tsql sql:
CREATE TABLE #TempTable (name VARCHAR(50), object_id INT, type_desc VARCHAR(50));
INSERT INTO #TempTable (name, object_id, type_desc)
VALUES ('TempTable', 1, 'USER_TABLE');
DECLARE @MyID INT;
SET @MyID = 1;
WITH temp_table AS (
    SELECT name, object_id, type_desc
    FROM #TempTable
)
SELECT name, object_id, type_desc
FROM temp_table
WHERE name = 'TempTable'
    AND object_id = @MyID;
SELECT *
FROM #TempTable;
-- REMORPH CLEANUP: DROP TABLE #TempTable;
