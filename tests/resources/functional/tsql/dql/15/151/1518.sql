-- tsql sql:
/* Declare a variable */
DECLARE @version VARCHAR(100);
/* Assign a value to the variable */
SET @version = '/*';
/* Use the variable in a query */
WITH temp_result AS (
  SELECT @@VERSION AS version
)
SELECT version FROM temp_result;
