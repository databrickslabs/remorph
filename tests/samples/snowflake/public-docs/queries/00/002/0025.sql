-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

-- First, use TIMESTAMP (mapped to TIMESTAMP_NTZ)

ALTER SESSION SET TIMESTAMP_TYPE_MAPPING = TIMESTAMP_NTZ;

CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP);

DESC TABLE ts_test;


-- Next, explicitly use one of the TIMESTAMP variations (TIMESTAMP_LTZ)

CREATE OR REPLACE TABLE ts_test(ts TIMESTAMP_LTZ);

DESC TABLE ts_test;
