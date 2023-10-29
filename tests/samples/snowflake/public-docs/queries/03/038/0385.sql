-- see https://docs.snowflake.com/en/sql-reference/functions/hll_accumulate

CREATE OR REPLACE TABLE test_table2 (c1 INTEGER);
-- Insert data.
INSERT INTO test_table2 (c1) SELECT c1 + 4 FROM sequence_demo;