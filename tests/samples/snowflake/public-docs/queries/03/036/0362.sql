-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table-column

CREATE OR REPLACE TABLE t1 (
   c1 NUMBER NOT NULL,
   c2 NUMBER DEFAULT 3,
   c3 NUMBER DEFAULT seq1.nextval,
   c4 VARCHAR(20) DEFAULT 'abcde',
   c5 STRING);

DESC TABLE t1;
