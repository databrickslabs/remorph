--Query type: DCL
SET DATEFIRST 4;
WITH temp_result AS (
    SELECT 'Spanish' AS language
)
SELECT language
FROM temp_result;