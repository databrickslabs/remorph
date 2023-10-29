-- see https://docs.snowflake.com/en/sql-reference/functions/regr_slope

select k, regr_slope(v, v2) from aggr group by k;
