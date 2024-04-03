
-- source:
SELECT TRY_TO_DATE('2023-25-09', 'yyyy-dd-MM');

-- databricks_sql:
SELECT DATE(TRY_TO_TIMESTAMP('2023-25-09', 'yyyy-dd-MM'));
