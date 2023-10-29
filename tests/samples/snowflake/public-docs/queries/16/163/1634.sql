-- see https://docs.snowflake.com/en/sql-reference/functions/hll_accumulate

SELECT hll_estimate(c1) FROM combined_resultstate;