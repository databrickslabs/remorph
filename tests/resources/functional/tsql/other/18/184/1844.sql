--Query type: DML
DECLARE @notastring INT;
SET @notastring = '1';
WITH temp_result AS (
    SELECT ' is not a string.' AS Result
)
SELECT @notastring + Result AS Result
FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
