-- see https://docs.snowflake.com/en/sql-reference/sql/drop-external-table

SHOW EXTERNAL TABLES LIKE 't2%';


DROP EXTERNAL TABLE t2;


SHOW EXTERNAL TABLES LIKE 't2%';
