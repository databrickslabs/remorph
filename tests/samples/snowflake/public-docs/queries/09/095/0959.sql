-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_estimate

SELECT APPROX_PERCENTILE_ESTIMATE(s , 0.01),
       APPROX_PERCENTILE_ESTIMATE(s , 0.15),
       APPROX_PERCENTILE_ESTIMATE(s , 0.845)
FROM testtable;