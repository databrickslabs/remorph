-- tsql sql:
DECLARE @var FLOAT;
SET @var = 10;
WITH temp_result AS (
    SELECT 1 AS id
)
SELECT 'The EXP of the variable is: ' + CONVERT(VARCHAR, EXP(@var))
FROM temp_result;
