-- see https://docs.snowflake.com/en/sql-reference/sql/create-sequence

CREATE OR REPLACE SEQUENCE seq_01 START = 1 INCREMENT = 1;
CREATE OR REPLACE TABLE sequence_test_table (i INTEGER);