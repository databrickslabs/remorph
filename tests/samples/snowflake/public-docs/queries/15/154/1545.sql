-- see https://docs.snowflake.com/en/sql-reference/functions/array_compact

SELECT array1, ARRAY_COMPACT(array1) FROM array_demo WHERE ID = 2;