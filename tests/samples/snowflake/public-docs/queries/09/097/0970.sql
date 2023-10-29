-- see https://docs.snowflake.com/en/sql-reference/functions/array_construct_compact

SELECT ARRAY_CONSTRUCT_COMPACT(null,'hello',3::double,4,5);