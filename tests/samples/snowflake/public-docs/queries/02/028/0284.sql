-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-event-table

CREATE OR REPLACE TABLE T1 (id NUMBER, date TIMESTAMP_NTZ, name STRING) CLUSTER BY (id, date);

SHOW TABLES LIKE 'T1';


-- Change the order of the clustering key
ALTER TABLE t1 CLUSTER BY (date, id);

SHOW TABLES LIKE 'T1';
