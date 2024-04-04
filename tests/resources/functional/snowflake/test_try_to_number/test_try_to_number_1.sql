
-- snowflake sql:
SELECT TRY_TO_DECIMAL('$345', '$999.00') AS col1;

-- databricks sql:
SELECT CAST(TRY_TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1;
