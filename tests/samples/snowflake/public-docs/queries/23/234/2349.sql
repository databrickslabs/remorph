-- see https://docs.snowflake.com/en/sql-reference/functions/strtok

select strtok('user@snowflake.com.', '@.', 4);