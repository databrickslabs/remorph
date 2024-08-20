
-- snowflake sql:
SELECT TRY_TO_DATE('2023-25-09', 'yyyy-dd-MM');

-- databricks sql:
SELECT DATE(TRY_TO_TIMESTAMP('2023-25-09', 'yyyy-dd-MM'));
