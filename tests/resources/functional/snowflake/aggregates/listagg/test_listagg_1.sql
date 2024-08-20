-- snowflake sql:
SELECT LISTAGG(col1, ' ') FROM test_table WHERE col2 > 10000;

-- databricks sql:
SELECT
  ARRAY_JOIN(ARRAY_AGG(col1), ' ')
FROM test_table
WHERE
  col2 > 10000
;
