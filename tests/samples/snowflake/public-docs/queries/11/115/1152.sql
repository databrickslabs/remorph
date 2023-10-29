-- see https://docs.snowflake.com/en/sql-reference/functions/array_size

SELECT GET(v, ARRAY_SIZE(v)-1) FROM colors;