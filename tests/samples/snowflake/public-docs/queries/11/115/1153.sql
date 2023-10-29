-- see https://docs.snowflake.com/en/sql-reference/functions/getbit

SELECT GETBIT(11, 100), GETBIT(11, 3), GETBIT(11, 2), GETBIT(11, 1), GETBIT(11, 0);