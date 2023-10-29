-- see https://docs.snowflake.com/en/sql-reference/functions/approx_top_k_estimate

SELECT approx_top_k_estimate(c1, 4) FROM combined_resultstate;