-- see https://docs.snowflake.com/en/sql-reference/functions/hll_combine

SELECT hll_estimate(c1) FROM combined_resultstate;