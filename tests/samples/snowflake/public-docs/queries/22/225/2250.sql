-- see https://docs.snowflake.com/en/sql-reference/functions/hash_agg

select hash_agg(null), hash_agg(null, null), hash_agg(null, null, null);
