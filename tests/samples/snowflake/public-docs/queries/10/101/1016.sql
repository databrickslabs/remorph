-- see https://docs.snowflake.com/en/sql-reference/functions/array_sort

SELECT ARRAY_SORT([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1e0::REAL]) AS array_of_different_numeric_types;