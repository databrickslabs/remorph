--Query type: DML
DECLARE @result VARCHAR(50);

-- Create a temporary result set using CTE identifier
WITH temp_result AS (
  SELECT 1 AS boolean_expression
)
-- Use the temporary result set in the query
SELECT
  @result = CASE
    WHEN boolean_expression = 1 THEN 'Boolean_expression is true.'
    ELSE 'Boolean_expression is false.'
  END
FROM temp_result;

PRINT @result;

-- REMORPH CLEANUP: DROP TABLE temp_result;
