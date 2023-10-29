-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_combine

CREATE OR REPLACE TABLE mytesttable AS
  SELECT APPROX_PERCENTILE_COMBINE(td) s FROM
    (
      (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) td FROM testtable WHERE c2 <= 0)
        UNION ALL
      (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) td FROM testtable WHERE c2 > 0 AND c2 <= 0.5)
        UNION ALL
      (SELECT APPROX_PERCENTILE_ACCUMULATE(C2) td FROM testtable WHERE c2 > 0.5)
    );

SELECT APPROX_PERCENTILE_ESTIMATE(s , 0.5) FROM mytesttable;