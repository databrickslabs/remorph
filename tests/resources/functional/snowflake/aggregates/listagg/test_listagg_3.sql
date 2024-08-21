-- snowflake sql:
SELECT LISTAGG(DISTINCT col3, '|')
            FROM test_table WHERE col2 > 10000;

-- databricks sql:
SELECT
  ARRAY_JOIN(ARRAY_AGG(DISTINCT col3), '|')
FROM test_table
WHERE
  col2 > 10000
;
