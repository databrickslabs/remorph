--Query type: DML
DECLARE @IntegerVariable INT;
SET @IntegerVariable = 123456;
SET @IntegerVariable = @IntegerVariable + 1;
WITH temp_result AS (
    SELECT CAST(@IntegerVariable AS BIGINT) AS result
)
SELECT result
FROM temp_result;
