
-- snowflake sql:
SELECT TO_DECIMAL('$345', '$999.00') AS col1;

-- databricks sql:
SELECT TO_NUMBER('$345', '$999.00') AS col1;
