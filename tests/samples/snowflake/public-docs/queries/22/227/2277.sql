-- see https://docs.snowflake.com/en/sql-reference/functions/regr_avgy

select k, regr_avgy(v, v2) from aggr group by k;
