
-- source:
SELECT LISTAGG(col1) FROM test_table;

-- databricks_sql:

        SELECT
          ARRAY_JOIN(ARRAY_AGG(col1), '')
        FROM test_table
        ;
