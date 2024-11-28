
-- snowflake sql:
SELECT TO_TIME('2018-05-15', 'yyyy-MM-dd');

-- databricks sql:
SELECT DATE_FORMAT(TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd'), 'HH:mm:ss');
