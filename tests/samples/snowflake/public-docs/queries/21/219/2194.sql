-- see https://docs.snowflake.com/en/sql-reference/functions/array_slice

select array_slice(array_construct(0,1,2,3,4,5,6), 0, 2);