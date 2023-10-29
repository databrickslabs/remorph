-- see https://docs.snowflake.com/en/sql-reference/functions/ceil

CREATE TRANSIENT TABLE test_ceiling (n FLOAT, scale INTEGER);
INSERT INTO test_ceiling (n, scale) VALUES
   (-975.975, -1),
   (-975.975,  0),
   (-975.975,  2),
   ( 135.135, -2),
   ( 135.135,  0),
   ( 135.135,  1),
   ( 135.135,  3),
   ( 135.135, 50),
   ( 135.135, NULL)
   ;