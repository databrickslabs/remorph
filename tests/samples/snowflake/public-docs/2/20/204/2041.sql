CREATE OR REPLACE TABLE resultstate2 AS 
  (SELECT approx_top_k_accumulate(c1, 50) AS rs1 
     FROM test_table2);