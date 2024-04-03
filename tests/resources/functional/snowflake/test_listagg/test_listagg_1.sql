
-- source:
SELECT LISTAGG(col1, ' ') FROM test_table WHERE col2 > 10000;

-- databricks_sql:

        SELECT
          ARRAY_JOIN(ARRAY_AGG(col1), ' ')
        FROM test_table
        WHERE
          col2 > 10000
        ;
