-- see https://docs.snowflake.com/en/sql-reference/functions/hll_accumulate

CREATE OR REPLACE TABLE resultstate1 AS (
     SELECT hll_accumulate(c1) AS rs1
        FROM sequence_demo);