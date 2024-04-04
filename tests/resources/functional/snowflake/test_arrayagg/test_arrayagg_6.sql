
-- snowflake sql:
SELECT ARRAY_AGG(col2) WITHIN GROUP (ORDER BY col2 DESC) FROM test_table;

-- databricks sql:
SELECT
              SORT_ARRAY(ARRAY_AGG(col2), FALSE)
            FROM test_table;
