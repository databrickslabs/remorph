
-- snowflake sql:
SELECT TO_TIME('2018-05-15 00:01:02');

-- databricks sql:
SELECT DATE_FORMAT(TO_TIMESTAMP('2018-05-15 00:01:02'), 'HH:mm:ss');
