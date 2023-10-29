-- see https://docs.snowflake.com/en/sql-reference/functions/array_append

SELECT ARRAY_APPEND(ARRAY_CONSTRUCT(1, 2, 3), 'HELLO');