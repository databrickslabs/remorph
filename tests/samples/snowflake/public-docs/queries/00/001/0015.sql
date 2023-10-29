-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile_accumulate

-- Create a table and insert some rows for which we'll later estimate the 
-- median value (the value at the 50th percentile).
CREATE OR REPLACE TABLE test_table1 (c1 INTEGER);
-- Insert data.
INSERT INTO test_table1 (c1) VALUES (1), (2), (3), (4);