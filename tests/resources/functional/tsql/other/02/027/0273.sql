--Query type: DDL
DECLARE @IsDataScientist BIT = 1;

WITH temp_result AS (
    SELECT 'value1' AS val
    UNION
    SELECT 'value2'
    UNION
    SELECT 'value3'
)

SELECT
    CASE
        WHEN @IsDataScientist = 1 THEN val
        ELSE '*******'
    END AS masked_val
FROM temp_result;
-- REMORPH CLEANUP: No objects were created, so no cleanup is necessary.
