-- see https://docs.snowflake.com/en/sql-reference/functions/array_flatten

SELECT ARRAY_FLATTEN([[1, 2, 3], NULL, [5, 6]]);