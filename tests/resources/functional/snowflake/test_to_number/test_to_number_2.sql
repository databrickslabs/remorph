
-- source:
SELECT TO_NUMERIC('$345', '$999.99') AS num;

-- databricks_sql:
SELECT TO_NUMBER('$345', '$999.99') AS num;
