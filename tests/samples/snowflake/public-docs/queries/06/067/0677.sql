-- see https://docs.snowflake.com/en/sql-reference/sql/insert

INSERT INTO mytable (col1, col3)
  SELECT TO_DATE('2013-05-08T23:39:20.123'), TO_TIMESTAMP('2013-05-08T23:39:20.123');

SELECT * FROM mytable;
