-- see https://docs.snowflake.com/en/sql-reference/functions/strtok

SELECT STRTOK('user@snowflake.com', '@.', 3);