-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-event-table

CREATE OR REPLACE TABLE t1(a1 number);

SHOW TABLES LIKE 't1';


ALTER TABLE t1 RENAME TO tt1;

SHOW TABLES LIKE 'tt1';
