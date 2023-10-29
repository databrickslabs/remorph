-- see https://docs.snowflake.com/en/sql-reference/functions/zeroifnull

SELECT column1, ZEROIFNULL(column1) 
    FROM VALUES (1), (null), (5), (0), (3.14159);