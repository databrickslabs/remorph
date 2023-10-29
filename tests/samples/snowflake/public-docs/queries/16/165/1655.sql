-- see https://docs.snowflake.com/en/sql-reference/functions/regr_avgx

SELECT k, REGR_AVGX(v, v2) FROM aggr GROUP BY k;
