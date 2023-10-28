CREATE OR REPLACE TABLE combined_resultstate (c1) AS 
  SELECT approx_percentile_combine(rs1) AS apc1
    FROM (
        SELECT rs1 FROM resultstate1
        UNION ALL
        SELECT rs1 FROM resultstate2
      )
      ;