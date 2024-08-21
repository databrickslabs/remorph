-- snowflake sql:
SELECT ARRAY_AGG(DISTINCT col2) WITHIN GROUP (ORDER BY col2 ASC)
FROM test_table
WHERE col3 > 10000;

-- databricks sql:
SELECT
  SORT_ARRAY(ARRAY_AGG(DISTINCT col2))
FROM test_table
WHERE
  col3 > 10000;
