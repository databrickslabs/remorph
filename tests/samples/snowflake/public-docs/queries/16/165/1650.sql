-- see https://docs.snowflake.com/en/sql-reference/functions/corr

SELECT k, CORR(v, v2) FROM aggr GROUP BY k;
