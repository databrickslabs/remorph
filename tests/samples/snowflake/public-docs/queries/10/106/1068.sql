-- see https://docs.snowflake.com/en/sql-reference/functions/count

SELECT COUNT(*), COUNT(i_col), COUNT(DISTINCT i_col), COUNT(j_col), COUNT(DISTINCT j_col) FROM basic_example;