-- see https://docs.snowflake.com/en/sql-reference/functions/square

SELECT column1, square(column1)
FROM (values (0), (1), (-2), (3.15), (null)) v;
