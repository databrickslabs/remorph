-- see https://docs.snowflake.com/en/sql-reference/functions/ifnull

SELECT a, b, IFNULL(a,b), IFNULL(b,a) FROM i;
