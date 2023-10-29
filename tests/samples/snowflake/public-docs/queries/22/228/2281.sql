-- see https://docs.snowflake.com/en/sql-reference/functions/regr_sxx

select k, regr_sxx(v, v2) from aggr group by k;
