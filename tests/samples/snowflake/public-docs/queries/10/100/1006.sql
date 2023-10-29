-- see https://docs.snowflake.com/en/sql-reference/functions/array_prepend

SELECT ARRAY_PREPEND(ARRAY_CONSTRUCT(0,1,2,3),'hello');