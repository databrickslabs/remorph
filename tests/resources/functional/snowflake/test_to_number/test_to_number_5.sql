
-- snowflake sql:
SELECT TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale;

-- databricks sql:
SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale;
