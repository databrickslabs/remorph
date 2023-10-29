-- see https://docs.snowflake.com/en/sql-reference/functions/stddev_pop

select k, stddev_pop(v), stddev_pop(v2) from aggr group by k;
