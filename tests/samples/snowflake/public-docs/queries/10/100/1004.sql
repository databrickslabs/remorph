-- see https://docs.snowflake.com/en/sql-reference/functions/array_position

SELECT ARRAY_POSITION('hello'::variant, array_construct('hola', 'bonjour'));