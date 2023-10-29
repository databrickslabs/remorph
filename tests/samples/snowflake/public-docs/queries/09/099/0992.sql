-- see https://docs.snowflake.com/en/sql-reference/functions/array_insert

SELECT ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),-1,'hello');