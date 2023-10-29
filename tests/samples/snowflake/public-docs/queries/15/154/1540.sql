-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_accumulate

SELECT approx_percentile_estimate(rs1, 0.5) 
    FROM resultstate1;