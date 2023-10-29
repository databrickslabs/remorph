-- see https://docs.snowflake.com/en/sql-reference/functions/approx_top_k_estimate

CREATE OR REPLACE TABLE test_table2 (c1 INTEGER);
-- Insert data.
INSERT INTO test_table2 (c1) SELECT c1 + 4 FROM sequence_demo;