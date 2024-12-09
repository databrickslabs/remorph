-- snowflake sql:
SELECT
        col1 AS ca
        FROM table1
        WHERE substr(ca,1,5) = '12345'
        ;

-- databricks sql:
SELECT
       col1 AS ca
       FROM table1
       WHERE SUBSTR(col1, 1,5) = '12345';
