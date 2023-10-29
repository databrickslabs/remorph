-- see https://docs.snowflake.com/en/sql-reference/functions/round

CREATE OR REPLACE TEMP TABLE rnd1(f float, d DECIMAL(10, 3));
INSERT INTO rnd1 (f, d) VALUES
      ( -10.005,  -10.005),
      (  -1.005,   -1.005),
      (   1.005,    1.005),
      (  10.005,   10.005)
      ;