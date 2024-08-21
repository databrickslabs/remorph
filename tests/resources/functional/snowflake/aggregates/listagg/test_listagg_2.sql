-- snowflake sql:
SELECT LISTAGG(col1) FROM test_table;

-- databricks sql:
SELECT
  ARRAY_JOIN(ARRAY_AGG(col1), '')
FROM test_table
;
