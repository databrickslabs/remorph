-- see https://docs.snowflake.com/en/sql-reference/functions/array_sort

SELECT ARRAY_SORT([20, PARSE_JSON('null'), 0, NULL, 10], TRUE, TRUE);