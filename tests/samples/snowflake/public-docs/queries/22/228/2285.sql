-- see https://docs.snowflake.com/en/sql-reference/functions/stddev_samp

select k, stddev_samp(v), stddev_samp(v2) from aggr group by k;
