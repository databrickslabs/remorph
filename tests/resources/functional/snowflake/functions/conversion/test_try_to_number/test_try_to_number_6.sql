
-- snowflake sql:
SELECT TRY_TO_DECIMAL('$755', '$999.00', 15, 5) AS num_with_scale;

-- databricks sql:
SELECT CAST(TRY_TO_NUMBER('$755', '$999.00') AS DECIMAL(15, 5)) AS num_with_scale;
