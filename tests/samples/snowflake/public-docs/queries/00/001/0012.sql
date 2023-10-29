-- see https://docs.snowflake.com/en/sql-reference/functions/hll_estimate

-- Create a sequence to use to generate values for the table.
CREATE OR REPLACE SEQUENCE seq92;
CREATE OR REPLACE TABLE sequence_demo (c1 INTEGER DEFAULT seq92.nextval, dummy SMALLINT);
INSERT INTO sequence_demo (dummy) VALUES (0);

-- Double the number of rows a few times, until there are 8 rows:
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;