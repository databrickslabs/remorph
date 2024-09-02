--Query type: DML
DECLARE @MyValue INT;
SET @MyValue = 3;
WITH temp AS (
    SELECT @MyValue * (7 + (9 - 4)) AS value
)
SELECT * FROM temp;