-- see https://docs.snowflake.com/en/sql-reference/functions/array_flatten

SELECT ARRAY_FLATTEN([[[1, 2], [3]], [[4], [5]]]);