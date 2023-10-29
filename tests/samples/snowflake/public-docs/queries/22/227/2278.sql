-- see https://docs.snowflake.com/en/sql-reference/functions/regr_intercept

select k, regr_intercept(v, v2) from aggr group by k;
