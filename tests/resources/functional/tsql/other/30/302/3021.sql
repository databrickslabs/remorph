--Query type: DCL
SET NOCOUNT ON;
WITH temp_result AS (
    SELECT 'NOCOUNT option is ON' AS message
)
SELECT *
FROM temp_result;
