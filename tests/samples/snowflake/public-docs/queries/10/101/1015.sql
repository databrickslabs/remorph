-- see https://docs.snowflake.com/en/sql-reference/functions/array_slice

SELECT ARRAY_SLICE(ARRAY_CONSTRUCT('foo','snow','flake','bar'), 1, 3);