-- tsql sql:
SET NOCOUNT ON;
WITH temp_result AS (
    SELECT 1 AS temp_column
)
SELECT *
FROM temp_result;
