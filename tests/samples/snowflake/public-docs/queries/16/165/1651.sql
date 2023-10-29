-- see https://docs.snowflake.com/en/sql-reference/functions/covar_pop

SELECT k, COVAR_POP(v, v2) FROM aggr GROUP BY k;
