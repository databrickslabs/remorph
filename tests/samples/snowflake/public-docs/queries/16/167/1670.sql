-- see https://docs.snowflake.com/en/sql-reference/functions/charindex

SELECT n, h, CHARINDEX(n, h) FROM pos;
