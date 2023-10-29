-- see https://docs.snowflake.com/en/sql-reference/sql/insert-multi-table

INSERT FIRST
  WHEN n1 > 100 THEN
    INTO t1
  WHEN n1 > 10 THEN
    INTO t1
    INTO t2
  ELSE
    INTO t2
SELECT n1 from src;