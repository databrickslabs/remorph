-- see https://docs.snowflake.com/en/sql-reference/functions/position

SELECT n, h, POSITION(n in h) FROM pos;
