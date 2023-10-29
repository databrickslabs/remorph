-- see https://docs.snowflake.com/en/sql-reference/functions/count_if

SELECT COUNT_IF(i_col IS NOT NULL AND j_col IS NOT NULL) FROM basic_example;