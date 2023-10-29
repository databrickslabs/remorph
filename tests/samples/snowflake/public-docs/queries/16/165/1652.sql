-- see https://docs.snowflake.com/en/sql-reference/functions/covar_samp

SELECT k, COVAR_SAMP(v, v2) FROM aggr GROUP BY k;

