-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile

SELECT APPROX_PERCENTILE(c1, 0.5) FROM testtable;