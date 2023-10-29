-- see https://docs.snowflake.com/en/sql-reference/functions/hash_agg

select year(o_orderdate), hash_agg(o_custkey, o_orderdate) from orders group by 1 order by 1;


select year(o_orderdate), hash_agg(distinct o_custkey, o_orderdate) from orders group by 1 order by 1;
