--Query type: DML
DECLARE @x10 INT = 42;
SET @x10 %= 3;
WITH temp AS (
    SELECT @x10 AS value
)
SELECT value FROM temp;
