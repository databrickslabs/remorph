--Query type: TCL
DECLARE @demo VARBINARY(8000);
SET @demo = (SELECT CONVERT(VARBINARY(8000), 'demo_value') AS value);
REVERT WITH COOKIE = @demo;
WITH temp_result AS (
  SELECT 'demo' AS column1, 'value' AS column2
)
SELECT SUSER_NAME(), USER_NAME(), temp_result.column1, temp_result.column2
FROM temp_result;
