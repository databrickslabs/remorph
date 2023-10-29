-- see https://docs.snowflake.com/en/sql-reference/functions/regr_sxy

select k, regr_sxy(v, v2) from aggr group by k;
