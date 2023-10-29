-- see https://docs.snowflake.com/en/sql-reference/functions/count_if

SELECT COUNT_IF(j_col > i_col) FROM basic_example;