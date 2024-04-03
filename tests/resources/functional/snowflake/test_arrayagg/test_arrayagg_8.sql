
-- source:
SELECT ARRAY_AGG(DISTINCT col2) WITHIN GROUP (ORDER BY col3 DESC) FROM test_table;

-- databricks_sql:
SELECT
                  SORT_ARRAY(ARRAY_AGG(DISTINCT col2), FALSE)
                FROM test_table;
