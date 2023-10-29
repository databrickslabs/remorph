-- see https://docs.snowflake.com/en/sql-reference/functions/greatest

SELECT
       col_1,
       col_2,
       col_3,
       GREATEST(col_1, col_2, col_3) AS greatest
   FROM test_table_1_greatest
   ORDER BY col_1;