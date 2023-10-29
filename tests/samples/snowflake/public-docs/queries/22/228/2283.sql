-- see https://docs.snowflake.com/en/sql-reference/functions/regr_syy

select k, regr_syy(v, v2) from aggr group by k;
