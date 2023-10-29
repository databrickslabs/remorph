-- see https://docs.snowflake.com/en/sql-reference/functions/hll_estimate

CREATE OR REPLACE TABLE resultstate2 AS 
  (SELECT hll_accumulate(c1) AS rs1 
     FROM test_table2);