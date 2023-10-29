-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_estimate

CREATE OR REPLACE TABLE resultstate AS (SELECT APPROX_PERCENTILE_ACCUMULATE(c1) s FROM testtable);