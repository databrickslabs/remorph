
-- source:
SELECT TRY_TO_DATE('2018-05-15');

-- databricks_sql:
SELECT DATE(TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd'));
