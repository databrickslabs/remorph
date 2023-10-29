-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_accumulate

SELECT approx_percentile_estimate(c1, 0.5) FROM combined_resultstate;