
-- source:
SELECT TRY_TO_NUMBER('$345', '$999.99') AS num;

-- databricks_sql:
SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num;
