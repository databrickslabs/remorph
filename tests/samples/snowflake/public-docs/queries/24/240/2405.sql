-- see https://docs.snowflake.com/en/sql-reference/functions/hash_agg

select year(o_orderdate), hash_agg(*) from orders group by 1 order by 1;
