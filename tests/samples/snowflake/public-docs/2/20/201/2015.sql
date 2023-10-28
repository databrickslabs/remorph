CREATE OR REPLACE TABLE resultstate1 AS (
     SELECT approx_percentile_accumulate(c1) AS rs1
        FROM test_table1);