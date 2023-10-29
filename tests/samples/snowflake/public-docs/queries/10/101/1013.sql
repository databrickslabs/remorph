-- see https://docs.snowflake.com/en/sql-reference/functions/array_size

SELECT ARRAY_SIZE(ARRAY_CONSTRUCT(1, 2, 3)) AS SIZE;