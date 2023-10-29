-- see https://docs.snowflake.com/en/sql-reference/functions/array_contains

SELECT ARRAY_CONTAINS('hello'::variant, array_construct('hello', 'hi'));