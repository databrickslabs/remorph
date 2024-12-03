--Query type: DML
DECLARE @notastring INT;
SET @notastring = 1;
WITH temp AS (
    SELECT @notastring AS id
)
SELECT id + 1
FROM temp
