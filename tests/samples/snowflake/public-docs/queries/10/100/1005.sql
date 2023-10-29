-- see https://docs.snowflake.com/en/sql-reference/functions/array_position

SELECT ARRAY_POSITION('hi'::variant, array_construct('hello', 'hi'));