-- see https://docs.snowflake.com/en/sql-reference/functions/hash_agg

select hash_agg(*) from orders;
