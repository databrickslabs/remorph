-- see https://docs.snowflake.com/en/sql-reference/functions/iff

select iff(NULL, 'true', 'false');