-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_accumulate

CREATE OR REPLACE TABLE resultstate2 AS 
  (SELECT approx_percentile_accumulate(c1) AS rs1 
     FROM test_table2);