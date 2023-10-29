-- see https://docs.snowflake.com/en/sql-reference/functions/array_construct

SELECT ARRAY_CONSTRUCT(null, 'hello', 3::double, 4, 5);