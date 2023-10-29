-- see https://docs.snowflake.com/en/sql-reference/functions/substr

SELECT SUBSTR('testing 1 2 3', 9, 5) FROM x;


SELECT '123456', pos, len, SUBSTR('123456', pos, len) FROM o;
