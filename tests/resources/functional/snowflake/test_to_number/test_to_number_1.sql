
-- source:
SELECT TO_DECIMAL('$345', '$999.00') AS col1;

-- databricks_sql:
SELECT TO_NUMBER('$345', '$999.00') AS col1;
