
-- snowflake sql:
SELECT TRY_TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale;

-- databricks sql:
SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale;
