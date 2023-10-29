-- see https://docs.snowflake.com/en/sql-reference/functions/in

SELECT (1, 2, 3) IN (
    SELECT col_1, col_2, col_3 FROM my_table
    ) AS RESULT;