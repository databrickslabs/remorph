-- see https://docs.snowflake.com/en/sql-reference/functions/to_array

SELECT array1, array2, ARRAY_CAT(array1, array2) FROM array_demo_2;