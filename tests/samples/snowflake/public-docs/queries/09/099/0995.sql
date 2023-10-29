-- see https://docs.snowflake.com/en/sql-reference/functions/array_sort

SELECT ARRAY_INSERT(ARRAY_INSERT(ARRAY_CONSTRUCT(), 3, 2), 6, 1) arr, ARRAY_SORT(arr);