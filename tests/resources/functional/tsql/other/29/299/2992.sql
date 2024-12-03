--Query type: DML
DECLARE @h INT;
SET @h = 4268;
WITH temp AS (
    SELECT @h AS value
)
SELECT *
FROM temp;
