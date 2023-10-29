-- see https://docs.snowflake.com/en/sql-reference/functions/approx_top_k_accumulate

CREATE OR REPLACE TABLE resultstate1 AS (
     SELECT approx_top_k_accumulate(c1, 50) AS rs1
        FROM sequence_demo);