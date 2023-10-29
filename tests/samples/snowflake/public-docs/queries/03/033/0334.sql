-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_combine

CREATE OR REPLACE TABLE mytest AS (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) s1 FROM testtable WHERE c2 < 0);

CREATE OR REPLACE TABLE mytest2 AS (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) s1 FROM testtable WHERE c2 >= 0);

CREATE OR REPLACE TABLE combinedtable AS
  SELECT APPROX_PERCENTILE_COMBINE(s) combinedstate FROM
    (
      (SELECT s1 s FROM mytest)
        UNION ALL
      (SELECT s1 s FROM mytest2)
    );

SELECT APPROX_PERCENTILE_ESTIMATE(combinedstate , 0.02) FROM combinedtable;