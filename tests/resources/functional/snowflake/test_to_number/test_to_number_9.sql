
-- source:
SELECT TO_DECIMAL('$345') AS col1;

-- databricks_sql:
SELECT CAST(TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1;
