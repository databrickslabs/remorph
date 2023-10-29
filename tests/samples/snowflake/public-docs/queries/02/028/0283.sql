-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table

CREATE OR REPLACE TABLE T1 (id NUMBER, date TIMESTAMP_NTZ, name STRING) CLUSTER BY (id, date);