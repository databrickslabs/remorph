-- see https://docs.snowflake.com/en/sql-reference/functions/timeadd

ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF9';
CREATE TABLE datetest (d date);
INSERT INTO datetest VALUES ('2013-04-05');