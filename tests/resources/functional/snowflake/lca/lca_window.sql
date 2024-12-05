-- snowflake sql:
SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
            ROW_NUMBER() OVER (PARTITION by ca ORDER BY t.col2 DESC) AS rn
        FROM table1 t;

-- databricks sql:
SELECT
            t.col1,
            t.col2,
            t.col3 AS ca,
            ROW_NUMBER() OVER (PARTITION by t.col3 ORDER BY t.col2 DESC NULLS FIRST) AS rn
        FROM table1 AS t;
