-- see https://docs.snowflake.com/en/sql-reference/functions/regr_r2

select k, regr_r2(v, v2) from aggr group by k;
